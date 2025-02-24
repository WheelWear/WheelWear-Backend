from django.contrib import admin
from .models import Cloth, ClothSubType, ClothClothSubType
from django.utils.html import format_html

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_preview', 'closet_category', 'size', 'cloth_type', 'isFavorite', 'get_cloth_subtypes', 'owner')
    search_fields = ('owner__username',)
    filter_horizontal = ('cloth_subtypes',)

    def get_cloth_subtypes(self, obj):
        return ", ".join([subtype.name for subtype in obj.cloth_subtypes.all()])
    get_cloth_subtypes.short_description = "Cloth Subtypes"
    
    def image_preview(self, obj):
        if obj.clothImage:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.clothImage.url)
        return "No Image"
    image_preview.short_description = 'Image Preview'

@admin.register(ClothClothSubType)
class ClothClothSubTypeAdmin(admin.ModelAdmin):
    list_display = ('cloth', 'clothSubType')  # Display cloth and its related subtypes

@admin.register(ClothSubType)
class ClothSubTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display cloth subtypes
