from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
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
        
        # 데이터 검증 및 수집
        validated_data = self._validate_and_collect_data(serializer, request.user)
        cloth_type = self._validate_clothing_combination(validated_data)

        # 기존 객체 조회 (이미 생성된 객체가 있다면 그대로 반환)
        existing_instance = self._get_existing_instance(validated_data)
        if existing_instance:
            output_serializer = self.get_serializer(existing_instance)
            return Response(output_serializer.data, status=status.HTTP_200_OK)

        # AI 이미지 URL 생성
        ai_result_image_url = self._generate_ai_image(validated_data, cloth_type)
        original_instance = validated_data.get('vton_image')

        if original_instance:
            # 원본 vton_image가 있을 경우 기존 객체를 복제하여 필요한 필드만 수정한 후 새 객체 생성
            new_instance = self._duplicate_instance_with_modifications(
                original_instance, validated_data, ai_result_image_url, request.user
            )
            output_serializer = self.get_serializer(new_instance)
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            # 원본 vton_image가 없는 경우, 일반 생성 로직 수행
            virtual_tryon = serializer.save(owner=request.user)
            virtual_tryon.image = ai_result_image_url
            virtual_tryon.save()
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def _get_existing_instance(self, validated_data):
        """
        기존 객체 조회를 위한 필터 조건 생성 후 기존 인스턴스 반환
        """
        filter_kwargs = self._build_filter_kwargs(validated_data)
        return VirtualTryOnImage.objects.filter(**filter_kwargs).exclude(image='').first()

    def _duplicate_instance_with_modifications(self, original_instance, validated_data, ai_result_image_url, user):
        """
        원본 vton_image 인스턴스를 기반으로 일부 필드를 수정하여 새 객체 생성
        """
        instance_data = {
            'top_cloth': validated_data.get('top_cloth') or original_instance.top_cloth,
            'bottom_cloth': validated_data.get('bottom_cloth') or original_instance.bottom_cloth,
            'dress_cloth': validated_data.get('dress_cloth') or original_instance.dress_cloth,
            'vton_image': original_instance,
            'body_image': None,  # vton_image를 사용하는 경우 body_image는 복제하지 않음.
            'image': ai_result_image_url,
            'owner': user,
        }
        return VirtualTryOnImage.objects.create(**instance_data)

    def _build_filter_kwargs(self, validated_data):
        """
        기존 객체 조회를 위한 필터 조건 생성
        """
        top_cloth = validated_data.get('top_cloth')
        bottom_cloth = validated_data.get('bottom_cloth')
        dress_cloth = validated_data.get('dress_cloth')
        body_image = validated_data.get('body_image')
        vton_image = validated_data.get('vton_image')

        filter_kwargs = {}
        if vton_image:
            filter_kwargs['vton_image'] = vton_image
        else:
            filter_kwargs['body_image'] = body_image

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
        """
        유저 소유권 검증 및 입력 데이터 수집
        """
        fields = {
            'top_cloth': "선택하신 상의는 본인의 옷이 아닙니다.",
            'bottom_cloth': "선택하신 하의는 본인의 옷이 아닙니다.",
            'dress_cloth': "선택하신 원피스는 본인의 옷이 아닙니다.",
            'body_image': "선택하신 원본 몸 사진은 본인의 사진이 아닙니다.",
            'vton_image': "선택하신 가상 사진은 본인의 사진이 아닙니다.",
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
        """
        의류 선택 조합 검증: 상의, 하의, 원피스 중 하나만 선택되었는지 확인
        """
        has_body = bool(validated_data.get('body_image'))
        has_top = bool(validated_data.get('top_cloth'))
        has_bottom = bool(validated_data.get('bottom_cloth'))
        has_dress = bool(validated_data.get('dress_cloth'))
        has_vton = bool(validated_data.get('vton_image'))

        if not (has_body or has_vton):
            raise ValidationError("본인의 사진을 입력해주세요.")
        if sum([has_top, has_bottom, has_dress]) != 1:
            raise ValidationError("상의, 하의, 원피스 중 하나만 선택해주세요.")

        if has_top:
            return 'Top'
        elif has_bottom:
            return 'Bottom'
        elif has_dress:
            return 'Dress'

    @staticmethod
    def _generate_ai_image(validated_data, cloth_type):
        """
        AI 서버를 호출하여 결과 이미지 URL을 생성
        """
        top_cloth = validated_data.get('top_cloth')
        bottom_cloth = validated_data.get('bottom_cloth')
        dress_cloth = validated_data.get('dress_cloth')
        body_image = validated_data.get('body_image')
        vton_image = validated_data.get('vton_image')

        try:
            new_image_url = get_ai_result_image(top_cloth, bottom_cloth, dress_cloth, body_image, vton_image, cloth_type)
            return new_image_url
        except Exception as e:
            raise ValidationError(f"AI 이미지 생성 실패: {str(e)}")
