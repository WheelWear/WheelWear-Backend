from rest_framework import generics, status
from .serializers import UserSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from .models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class ProfileDetailView(APIView):
    def get(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = request.user.profile
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # serializer의 save()메소드를 호출하면 내부 함수인 create() 메서드가 작동한다.
        user = serializer.save() 
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User created successfully",
        }, status=status.HTTP_201_CREATED)
        


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer