from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class ProfileSerializer(serializers.ModelSerializer):
    # 읽기 전용 필드 (계산된 속성)
    age = serializers.ReadOnlyField()  # Age is a calculated field.
    is_reform_provider = serializers.ReadOnlyField()
    
    class Meta:
        model = Profile
        fields = ['name', 'gender', 'birth_date', 'age', 'bio', 'phone_number', 'profile_picture', 'is_reform_provider']


class UserSerializer(serializers.ModelSerializer):
    realname = serializers.CharField(write_only=True)  # 모델에 없으므로 write_only로 처리
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'realname', 'date_joined','last_login')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        first_name = validated_data.get('realname', '-')  # realname을 first_name으로 처리
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=first_name,
        )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    profile = ProfileSerializer(source='user.profile', read_only=True)  # 프로필 직렬화기 추가

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # 기본 사용자 정보
        data.update({
            'username': self.user.username,
            'id': self.user.id,
            'date_joined': self.user.date_joined
        })
        
        # 프로필 정보 추가 (시리얼라이저 활용)
        data['profile'] = ProfileSerializer(self.user.profile).data
        
        return data