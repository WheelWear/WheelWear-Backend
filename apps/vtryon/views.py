from rest_framework import generics, permissions, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from .models import BodyImage, VirtualTryOnImage
from .serializers import BodyImageSerializer
from .serializers import (
    VirtualTryOnImageListSerializer,
    VirtualTryOnImageCreateUpdateSerializer,
    VirtualTryOnImageDetailSerializer
)
from .permissions import IsOwner
from clothing.models import Cloth

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
    VirtualTryOnImage에 대해 전체 CRUD 기능을 제공하며,
    - list: 간단한 정보(PK 형태의 외래키)만 보여줌
    - retrieve(디테일뷰): top_cloth, bottom_cloth, body_image의 상세 정보를 (소유자 제외) JSON 형태로 표시
    - create/update: 해당 외래키들이 현재 로그인 사용자의 소유인지 검증 후 저장
    """
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # 현재 사용자가 소유한 VirtualTryOnImage만 조회합니다.
        return VirtualTryOnImage.objects.filter(owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return VirtualTryOnImageListSerializer
        elif self.action == 'retrieve':
            return VirtualTryOnImageDetailSerializer
        else:
            return VirtualTryOnImageCreateUpdateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        # 생성 시 입력받은 객체들을 가져옵니다.
        top_cloth = serializer.validated_data.get('top_cloth')
        bottom_cloth = serializer.validated_data.get('bottom_cloth')
        body_image = serializer.validated_data.get('body_image')

        # 각 객체의 소유자가 현재 사용자와 일치하는지 검증합니다.
        if top_cloth and top_cloth.owner != user:
            raise PermissionDenied("선택하신 상의는 본인의 옷이 아닙니다.")
        if bottom_cloth and bottom_cloth.owner != user:
            raise PermissionDenied("선택하신 하의는 본인의 옷이 아닙니다.")
        if body_image and body_image.owner != user:
            raise PermissionDenied("선택하신 원본 몸 사진은 본인의 사진이 아닙니다.")

        serializer.save(owner=user)

    def perform_update(self, serializer):
        user = self.request.user
        # partial_update의 경우 기존 객체의 값을 fallback합니다.
        top_cloth = serializer.validated_data.get('top_cloth', serializer.instance.top_cloth)
        bottom_cloth = serializer.validated_data.get('bottom_cloth', serializer.instance.bottom_cloth)
        body_image = serializer.validated_data.get('body_image', serializer.instance.body_image)

        # 업데이트 시에도 각 객체의 소유자가 현재 사용자와 일치하는지 검증합니다.
        if top_cloth and top_cloth.owner != user:
            raise PermissionDenied("선택하신 상의는 본인의 옷이 아닙니다.")
        if bottom_cloth and bottom_cloth.owner != user:
            raise PermissionDenied("선택하신 하의는 본인의 옷이 아닙니다.")
        if body_image and body_image.owner != user:
            raise PermissionDenied("선택하신 원본 몸 사진은 본인의 사진이 아닙니다.")

        serializer.save(owner=user)