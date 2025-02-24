from django.contrib import admin
from .models import Profile
from django.utils.html import format_html

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'gender', 'profile_picture')  # 관리자 페이지에 표시할 필드
    search_fields = ('user__username', 'name')  # 검색 가능 필드
    
    def image_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.profile_picture.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'