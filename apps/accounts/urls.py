from django.urls import path
from rest_framework_simplejwt.views import (
    # TokenObtainPairView, # 로그인을 위한 뷰
    TokenRefreshView, # 토큰 갱신을 위한 뷰
    TokenVerifyView, # 토큰 검증을 위한 뷰
    TokenBlacklistView  # 로그아웃을 위한 뷰
)
from .views import RegisterView, ProfileDetailView, CustomTokenObtainPairView
# https://jwt.io/를 통해 jwt의 내용을 해석가능

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('profile/', ProfileDetailView.as_view(), name='profile-detail'),
]
