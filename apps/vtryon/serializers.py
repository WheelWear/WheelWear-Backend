from rest_framework import serializers
from django.apps import apps
from .models import BodyImage, VirtualTryOnImage
from clothing.serializers import ClothSerializer

Cloth = apps.get_model('clothing', 'Cloth')

class BodyImageSerializer(serializers.ModelSerializer):
    # owner는 읽기 전용으로 처리하거나, 필요에 따라 상세 정보를 넣을 수 있습니다.
    owner = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = BodyImage
        fields = ['id','gender', 'chest_circumference','shoulder_width','arm_length','waist_circumference', 'owner', 'body_image', 'title', 'created_at', 'is_favorite']

# 조회용
class VirtualTryOnImageListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    top_cloth = serializers.PrimaryKeyRelatedField(read_only=True)
    bottom_cloth = serializers.PrimaryKeyRelatedField(read_only=True)
    body_image = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VirtualTryOnImage
        fields = [
            'id', 'owner', 'image', 'title',
            'top_cloth', 'bottom_cloth', 'body_image',
            'dress_cloth', 
            'is_favorite', 'created_at', 'uploaded_at', 'saved'
        ]
        
# 생성용, 수정용, 삭제용 Serializers
class VirtualTryOnImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTryOnImage
        fields = [
            'image', 
            'title', 
            'top_cloth', 
            'bottom_cloth', 
            'dress_cloth', 
            'body_image', 
            'is_favorite', 
            'saved'
        ]
        read_only_fields = ['image']  # 사용자 입력을 막기 위해 read_only 설정
        
#########################################
# (2) 디테일(detail)용 Nested Serializer
#########################################

# VirtualTryOnImage 디테일 Serializer: 각 외래키를 위의 nested serializer로 표시.
class VirtualTryOnImageDetailSerializer(serializers.ModelSerializer):
    top_cloth = ClothSerializer(read_only=True)
    bottom_cloth = ClothSerializer(read_only=True)
    body_image = BodyImageSerializer(read_only=True)

    class Meta:
        model = VirtualTryOnImage
        fields = [
            'id', 'image', 'title',
            'dress_cloth', 
            'top_cloth', 'bottom_cloth', 'body_image',
            'is_favorite', 'created_at', 'uploaded_at', 'saved'
        ]