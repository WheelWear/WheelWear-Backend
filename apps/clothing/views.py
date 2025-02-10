from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cloth, ClothSubType
from .serializers import ClothSerializer, ClothSubTypeSerializer
from .permissions import IsOwner, IsAdmin # Custom Permission 가져오기

class ClothViewSet(viewsets.ModelViewSet):
    queryset = Cloth.objects.all()
    serializer_class = ClothSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]  # 추가

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