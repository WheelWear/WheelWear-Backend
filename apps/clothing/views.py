from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .models import Cloth, ClothSubType
from .serializers import ClothSerializer, ClothSubTypeSerializer
from .permissions import IsOwner, IsAdmin # Custom Permission 가져오기
from .services import get_ai_result

class ClothViewSet(viewsets.ModelViewSet):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]  # 추가

    @action(detail=True, methods=['post'], url_path='size')
    def size(self, request, pk=None):
        """
        clothID에 해당하는 의류의 AI 추천 사이즈 결과를 가져와 반환합니다.
        요청 사용자의 신체 정보를 기반으로 AI 서버에 데이터를 전송하며,
        통신 오류나 데이터 누락 시 적절한 예외를 처리합니다.
        """
        try:
            cloth = self.get_object()
        except Exception as e:
            raise APIException(f"해당 의류 정보를 가져오는 중 문제가 발생했습니다: {str(e)}")
        
        # 요청 사용자의 신체 정보 확인
        try:
            my_info = request.user.body_images
        except AttributeError:
            return Response(
                {"detail": "사용자 신체 정보가 존재하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # AI 서버와 통신하여 추천 결과를 가져옴
            ai_result = get_ai_result(
                brand=cloth.brand,
                cloth_size=cloth.size,
                cloth_type=cloth.cloth_type,
                gender=my_info.gender,
                chest_circumference=my_info.chest_circumference,
                shoulder_width=my_info.shoulder_width,
                arm_length=my_info.arm_length,
                waist_circumference=my_info.waist_circumference,
                request=request
            )
        except Exception as e:
            return Response(
                {"detail": f"AI 서버와 통신 중 문제가 발생했습니다: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(ai_result, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        # 현재 로그인한 사용자를 소유자로 설정
        serializer.save(owner=self.request.user)
        
    # 현재 사용자의 옷만 필터링
    def get_queryset(self):
        return Cloth.objects.filter(owner=self.request.user)

class ClothSubTypeViewSet(viewsets.ModelViewSet):
    queryset = ClothSubType.objects.all()
    serializer_class = ClothSubTypeSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]