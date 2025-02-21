from django.db import models
from django.conf import settings

# BodyImage: 사용자의 원본 몸 사진
class BodyImage(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='body_images'
    )
    body_image = models.ImageField(upload_to='body_images/')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    chest_circumference = models.IntegerField(null=True, blank=True)
    shoulder_width = models.IntegerField(null=True, blank=True)
    arm_length = models.IntegerField(null=True, blank=True)
    waist_circumference = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return self.title


# VirtualTryOnImage: AI로 생성된 가상의류 시착 이미지
class VirtualTryOnImage(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='virtual_tryon_images'
    )
    saved = models.BooleanField(default=False)
    image = models.CharField(max_length=255, null=False, blank=False)
    title = models.CharField(max_length=255)
    top_cloth = models.ForeignKey(
        'clothing.Cloth',
        on_delete=models.CASCADE,
        related_name='top_virtual_tryon_images',
        null=True
    )
    bottom_cloth = models.ForeignKey(
        'clothing.Cloth',
        on_delete=models.CASCADE,
        related_name='bottom_virtual_tryon_images',
        null=True
    )
    dress_cloth = models.ForeignKey(
        'clothing.Cloth',
        on_delete=models.CASCADE,
        related_name='dress_virtual_tryon_images',
        null=True
    )
    
    # 사용된 원본 BodyImage
    body_image = models.ForeignKey(
        BodyImage,
        on_delete=models.CASCADE,
        related_name='virtual_tryon_images',
        null=True
    )
    
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"VirtualTryOnImage by {self.owner}"
