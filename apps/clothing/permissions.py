# clothing/permissions.py
from rest_framework import permissions
    
class IsOwner(permissions.BasePermission):
    """
    조회는 누구나 가능, 객체 소유자만 객체의 RUD 기능을 사용 가능.
    """
    def has_object_permission(self, request, view, obj):
        # 작성자만 CRUD 가능
        return obj.owner == request.user


class IsAdmin(permissions.BasePermission):
    """
    조회는 누구나 가능, 나머지는 관리자만 가능
    """
    def has_permission(self, request, view):
        # 뷰 전체에 대한 접근 권한을 체크 (예: 목록 조회, 생성).
        print(request.user.is_staff, request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    def has_object_permission(self, request, view, obj):
        # 특정 객체에 대한 접근 권한을 체크 (예: 상세 조회, 수정, 삭제).
        print(request.user.is_staff, request.method)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    

class IsAdminOrReadOrPatchOnly(permissions.BasePermission):
    """
    GET, HEAD, OPTIONS: 모든 사용자 허용
    PATCH: 인증된 사용자 허용
    POST, PUT, DELETE: 관리자만 허용
    """
    def has_permission(self, request, view):
        # SAFE_METHODS (GET, HEAD, OPTIONS) 또는 PATCH 허용
        if request.method in permissions.SAFE_METHODS or request.method == 'PATCH':
            return True
        # 그 외 작업은 관리자만 허용
        return request.user and request.user.is_staff

    def has_object_permission(self, request, view, obj):
        # PATCH는 본인만 허용 (선택적)
        if request.method == 'PATCH':
            return obj.owner == request.user
        return super().has_object_permission(request, view, obj)