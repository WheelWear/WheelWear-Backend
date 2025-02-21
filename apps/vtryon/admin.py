from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import BodyImage, VirtualTryOnImage

class BodyImageAdmin(admin.ModelAdmin):
    list_display = ('title','gender', 'chest_circumference','shoulder_width','arm_length','waist_circumference', 'owner', 'created_at', 'is_favorite', 'image_preview')
    list_filter = ('owner', 'created_at', 'is_favorite')
    search_fields = ('title', 'owner__username')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.body_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.body_image)
        return "No Image"
    image_preview.short_description = 'Image Preview'

class VirtualTryOnImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at', 'is_favorite', 
                'top_cloth', 'bottom_cloth', 'dress_cloth', 'body_image', 'image_preview', 'saved')
    list_filter = ('owner', 'created_at', 'is_favorite', 
                'top_cloth', 'bottom_cloth')
    search_fields = ('title', 'owner__username', 
                    'top_cloth__name', 'bottom_cloth__name')
    raw_id_fields = ('top_cloth', 'bottom_cloth', 'body_image')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image)
        return "No Image"
    image_preview.short_description = 'Image Preview'

admin.site.register(BodyImage, BodyImageAdmin)
admin.site.register(VirtualTryOnImage, VirtualTryOnImageAdmin)