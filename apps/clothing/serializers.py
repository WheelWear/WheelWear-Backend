# clothing/serializers.py
from rest_framework import serializers
from django.db import transaction
from .models import Cloth, ClothSubType, ClothSubType
from rest_framework.exceptions import ValidationError

class ClothSubTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClothSubType
        fields = ['id', 'name']
        read_only_fields = ['id']
    

class ClothSerializer(serializers.ModelSerializer):
    cloth_subtypes_names = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        help_text="태그 이름을 쉼표(,)로 구분한 문자열 (예: '스트릿,루즈핏')"
    )
    cloth_subtypes = serializers.SlugRelatedField(  # 태그 이름 목록을 읽기 전용으로 표시
        many=True,
        slug_field='name',
        read_only=True,
        help_text="태그 이름 리스트 (읽기 전용)"
    )

    class Meta:
        model = Cloth
        fields = [
            'id', 
            'clothImage', 
            'type', 
            'isFavorite', 
            'createdAt', 
            'owner', 
            'cloth_subtypes', 
            'cloth_subtypes_names'
        ]
        read_only_fields = ['owner', 'createdAt']  # createdAt도 일반적으로 읽기 전용

    def create(self, validated_data):
        # 태그 이름 리스트 추출 (기본값: 빈 리스트)
        subtype_names = validated_data.pop('cloth_subtypes_names', [])
        
        # 태그 객체 조회 또는 생성
        subtypes = []
        for name in subtype_names.split(','):
            try:
                subtype = ClothSubType.objects.get(name=name)
                subtypes.append(subtype)
            except ClothSubType.DoesNotExist:
                raise ValidationError(f"ClothSubType '{name}' does not exist")
        
        # 옷 객체 생성
        cloth = Cloth.objects.create(**validated_data)
        
        # M2M 관계 설정
        cloth.cloth_subtypes.set(subtypes)
        return cloth

    def update(self, instance, validated_data):
        try:
            # 트랜잭션 시작 (원자적 작업 보장)
            with transaction.atomic():
                # 태그 이름 리스트 추출 (None 체크로 부분 업데이트 지원)
                subtype_names = validated_data.pop('cloth_subtypes_names', None)
                
                # 필드 업데이트
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                # 태그 업데이트 (값이 제공된 경우에만)
                if subtype_names is not None:
                    subtypes = []
                    for name in subtype_names.split(','):
                        try:
                            subtype = ClothSubType.objects.get(name=name)
                            subtypes.append(subtype)
                        except ClothSubType.DoesNotExist:
                            raise ValidationError(f"ClothSubType '{name}' does not exist")
                        
                    instance.cloth_subtypes.set(subtypes)
                
                return instance
        except Exception as e:
            # 트랜잭션 롤백 및 에러 전파
            if isinstance(e, ValidationError):
                raise  # DRF ValidationError는 그대로 전달
            else:
                # 기타 예외는 500 에러로 처리
                raise serializers.ValidationError("Internal server error") from e