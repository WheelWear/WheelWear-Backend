from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender')  # 관리자 페이지에 표시할 필드
    search_fields = ('user__username', 'name')  # 검색 가능 필드