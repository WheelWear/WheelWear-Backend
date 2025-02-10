from django.contrib import admin
from .models import Cloth, ClothSubType, ClothClothSubType

@admin.register(Cloth)
class ClothAdmin(admin.ModelAdmin):
    list_display = ('id', 'clothImage', 'type', 'isFavorite', 'get_cloth_subtypes', 'owner')  # Display related subtypes
    search_fields = ('owner__username',)  # Search by owner's username
    filter_horizontal = ('cloth_subtypes',)  # Makes ManyToMany easier to manage

    def get_cloth_subtypes(self, obj):
        return ", ".join([subtype.name for subtype in obj.cloth_subtypes.all()])  # Display comma-separated cloth subtypes
    get_cloth_subtypes.short_description = "Cloth Subtypes"

@admin.register(ClothClothSubType)
class ClothClothSubTypeAdmin(admin.ModelAdmin):
    list_display = ('cloth', 'clothSubType')  # Display cloth and its related subtypes

@admin.register(ClothSubType)
class ClothSubTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display cloth subtypes
