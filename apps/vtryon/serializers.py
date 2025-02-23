from rest_framework import serializers
from django.apps import apps
from .models import BodyImage, VirtualTryOnImage
from clothing.serializers import ClothSerializer

Cloth = apps.get_model('clothing', 'Cloth')


class BodyImageSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = BodyImage
        fields = [
            'id', 'gender', 'chest_circumference', 'shoulder_width',
            'arm_length', 'waist_circumference', 'owner', 'body_image',
            'title', 'created_at', 'is_favorite'
        ]


class VirtualTryOnImageListSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    top_cloth = serializers.PrimaryKeyRelatedField(read_only=True)
    bottom_cloth = serializers.PrimaryKeyRelatedField(read_only=True)
    dress_cloth = serializers.PrimaryKeyRelatedField(read_only=True)
    vton_image = serializers.PrimaryKeyRelatedField(read_only=True)
    body_image = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = VirtualTryOnImage
        fields = [
            'id', 'owner', 'vton_image', 'image', 'title',
            'top_cloth', 'bottom_cloth', 'body_image',
            'dress_cloth', 'is_favorite', 'created_at', 'uploaded_at', 'saved'
        ]


class VirtualTryOnImageCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualTryOnImage
        fields = [
            'image', 'title', 'vton_image', 'top_cloth', 
            'bottom_cloth', 'dress_cloth', 'body_image', 
            'is_favorite', 'saved'
        ]
        read_only_fields = ['image']  # AI 이미지 결과로 채워지므로 외부 입력은 막음


class VirtualTryOnImageDetailSerializer(serializers.ModelSerializer):
    top_cloth = ClothSerializer(read_only=True)
    bottom_cloth = ClothSerializer(read_only=True)
    body_image = BodyImageSerializer(read_only=True)
    # vton_image를 상세보기용으로 Nested 처리
    vton_image = VirtualTryOnImageListSerializer(read_only=True)

    class Meta:
        model = VirtualTryOnImage
        fields = [
            'id', 'image', 'title', 'dress_cloth', 'vton_image',
            'top_cloth', 'bottom_cloth', 'body_image',
            'is_favorite', 'created_at', 'uploaded_at', 'saved'
        ]