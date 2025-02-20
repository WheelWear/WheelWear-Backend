from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import BodyImage, VirtualTryOnImage
from .serializers import BodyImageSerializer
from .services import get_ai_result_image
from .serializers import (
    VirtualTryOnImageListSerializer,
    VirtualTryOnImageCreateUpdateSerializer,
    VirtualTryOnImageDetailSerializer
)
from .permissions import IsOwner

class BodyImageViewSet(viewsets.ModelViewSet):
    queryset = BodyImage.objects.all()
    serializer_class = BodyImageSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    def get_queryset(self):
        return BodyImage.objects.filter(owner=self.request.user)

class VirtualTryOnImageViewSet(viewsets.ModelViewSet):
    """
    VirtualTryOnImage에 대해 전체 CRUD 기능을 제공
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return VirtualTryOnImage.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return VirtualTryOnImageListSerializer
        elif self.action == 'retrieve':
            return VirtualTryOnImageDetailSerializer
        else:
            return VirtualTryOnImageCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = self._validate_and_collect_data(serializer, request.user)
        self._validate_clothing_combination(validated_data)

        # 기존 객체 조회
        filter_kwargs = self._build_filter_kwargs(validated_data)
        existing_instance = VirtualTryOnImage.objects.filter(**filter_kwargs).exclude(image='').first()
        if existing_instance:
            output_serializer = self.get_serializer(existing_instance)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        # 없으면 생성 진행
        self._process_ai(serializer, request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _process_ai(self, serializer, user, instance=None):
        """
        공통 AI 이미지 처리 및 모델 저장 로직
        """
        validated_data = self._validate_and_collect_data(serializer, user, instance)
        self._validate_clothing_combination(validated_data)

        # AI 서버에서 이미지 URL 가져오기
        ai_result_image_url = self._generate_ai_image(validated_data)

        # 모델 인스턴스 저장
        virtual_tryon = serializer.save(owner=user)
        
        virtual_tryon.image = ai_result_image_url
        virtual_tryon.save()

        # return virtual_tryon


    def _build_filter_kwargs(self, validated_data):
        """ 기존 객체 조회를 위한 필터 조건 생성 """
        top_cloth = validated_data.get('top_cloth')
        bottom_cloth = validated_data.get('bottom_cloth')
        dress_cloth = validated_data.get('dress_cloth')
        body_image = validated_data.get('body_image')

        filter_kwargs = {'body_image': body_image}
        if dress_cloth:
            filter_kwargs['dress_cloth'] = dress_cloth
        else:
            if top_cloth:
                filter_kwargs['top_cloth'] = top_cloth
            else:
                filter_kwargs['top_cloth__isnull'] = True

            if bottom_cloth:
                filter_kwargs['bottom_cloth'] = bottom_cloth
            else:
                filter_kwargs['bottom_cloth__isnull'] = True

        return filter_kwargs

    @staticmethod
    def _validate_and_collect_data(serializer, user, instance=None):
        """ 유저 소유권 검증 및 데이터 수집 """
        fields = {
            'top_cloth': "선택하신 상의는 본인의 옷이 아닙니다.",
            'bottom_cloth': "선택하신 하의는 본인의 옷이 아닙니다.",
            'dress_cloth': "선택하신 원피스는 본인의 옷이 아닙니다.",
            'body_image': "선택하신 원본 몸 사진은 본인의 사진이 아닙니다."
        }

        validated_data = {}
        for field, error_message in fields.items():
            obj = serializer.validated_data.get(field, getattr(instance, field, None) if instance else None)
            if obj and obj.owner != user:
                raise PermissionDenied(error_message)
            validated_data[field] = obj

        return validated_data

    @staticmethod
    def _validate_clothing_combination(validated_data):
        """ 의류 선택 조합 검증 """
        has_body = bool(validated_data.get('body_image'))
        has_top = bool(validated_data.get('top_cloth'))
        has_bottom = bool(validated_data.get('bottom_cloth'))
        has_dress = bool(validated_data.get('dress_cloth'))

        if not any([has_top, has_bottom, has_dress]):
            raise ValidationError("상의, 하의 또는 원피스 중 하나를 선택해야 합니다.")
        if not has_body:
            raise ValidationError("본인의 사진을 입력해주세요.")

        if has_dress and (has_top or has_bottom):
            message = (
                "상의, 하의, 원피스를 모두 선택할 수 없습니다."
                if (has_top and has_bottom) else
                "상의와 하의를 선택하면 원피스를 선택할 수 없습니다."
            )
            raise ValidationError(message)

    @staticmethod
    def _generate_ai_image(validated_data):
        """
        AI 결과 이미지 생성
        """
        top_cloth = validated_data.get('top_cloth')
        bottom_cloth = validated_data.get('bottom_cloth')
        dress_cloth = validated_data.get('dress_cloth')
        body_image = validated_data.get('body_image')

        filter_kwargs = {'body_image': body_image}
        if dress_cloth:
            filter_kwargs['dress_cloth'] = dress_cloth
        else:
            if top_cloth:
                filter_kwargs['top_cloth'] = top_cloth
            else:
                filter_kwargs['top_cloth__isnull'] = True
            if bottom_cloth:
                filter_kwargs['bottom_cloth'] = bottom_cloth
            else:
                filter_kwargs['bottom_cloth__isnull'] = True

        existing = VirtualTryOnImage.objects.filter(**filter_kwargs).exclude(image='').first()
        if existing:
            return existing.image

        try:
            new_image_url = get_ai_result_image(top_cloth, bottom_cloth, dress_cloth, body_image)
            return new_image_url
        except Exception as e:
            raise ValidationError(f"AI 이미지 생성 실패: {str(e)}")
