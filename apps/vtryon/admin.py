from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import BodyImage, VirtualTryOnImage

class BodyImageAdmin(admin.ModelAdmin):
    list_display = ('owner', 'image_preview', 'title', 'gender', 'chest_circumference','shoulder_width','arm_length','waist_circumference', 'created_at', 'is_favorite')
    list_filter = ('owner', 'created_at', 'is_favorite')
    search_fields = ('title', 'owner__username')
    readonly_fields = ('image_preview',)
    
    def image_preview(self, obj):
        if obj.body_image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.body_image.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

class VirtualTryOnImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'owner',
        'result_image_preview',
        'created_at',
        'is_favorite',
        'vton_image_preview',
        'body_image_preview',
        'top_cloth_preview',
        'bottom_cloth_preview',
        'dress_cloth_preview',
        'saved'
    )
    list_filter = ('owner', 'created_at', 'is_favorite', 'top_cloth', 'bottom_cloth')
    search_fields = ('title', 'owner__username', 'top_cloth__name', 'bottom_cloth__name')
    raw_id_fields = ('top_cloth', 'bottom_cloth', 'body_image')
    readonly_fields = (
        'result_image_preview',
        'vton_image_preview',
        'top_cloth_preview',
        'bottom_cloth_preview',
        'dress_cloth_preview',
        'body_image_preview',
    )
    
    def result_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image)
        return "No Image"
    result_image_preview.short_description = 'result Image'
    
    def vton_image_preview(self, obj):
        if obj.vton_image and obj.vton_image.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.vton_image.image)
        return "No Image"
    vton_image_preview.short_description = 'VTON Image'
    
    def top_cloth_preview(self, obj):
        if obj.top_cloth and hasattr(obj.top_cloth.clothImage, 'url'):
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.top_cloth.clothImage.url)
        return "No Image"
    top_cloth_preview.short_description = 'Top Cloth'
    
    def bottom_cloth_preview(self, obj):
        if obj.bottom_cloth and hasattr(obj.bottom_cloth.clothImage, 'url'):
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.bottom_cloth.clothImage.url)
        return "No Image"
    bottom_cloth_preview.short_description = 'Bottom Cloth'
    
    def dress_cloth_preview(self, obj):
        if obj.dress_cloth and hasattr(obj.dress_cloth.clothImage, 'url'):
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.dress_cloth.clothImage.url)
        return "No Image"
    dress_cloth_preview.short_description = 'Dress Cloth'
    
    def body_image_preview(self, obj):
        if obj.body_image and hasattr(obj.body_image.body_image, 'url'):
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.body_image.body_image.url)
        return "No Image"
    body_image_preview.short_description = 'Body Image'

admin.site.register(BodyImage, BodyImageAdmin)
admin.site.register(VirtualTryOnImage, VirtualTryOnImageAdmin)