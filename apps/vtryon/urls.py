from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BodyImageViewSet, VirtualTryOnImageViewSet

router = DefaultRouter()
router.register(r'body-images', BodyImageViewSet, basename='bodyimage')
router.register(r'virtual-tryon-images', VirtualTryOnImageViewSet, basename='virtualtryonimage')

urlpatterns = [
    path('', include(router.urls)),
]
