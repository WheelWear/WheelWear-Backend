from django.db import models
from django.conf import settings

class ClothType(models.TextChoices):
    TOP = 'Top', 'Top'
    BOTTOM = 'Bottom', 'Bottom'
    DRESS = 'Dress', 'Dress'

# class ClothSubTypeEnum(models.TextChoices):
#     JEANS = 'Jeans', 'Jeans'
#     SHORTS = 'Shorts', 'Shorts'
#     TSHIRT = 'TShirt', 'TShirt'
#     HOODIE = 'Hoodie', 'Hoodie'
#     SPORTSWEAR_TOP = 'SportswearTop', 'SportswearTop'
#     SPORTSWEAR_BOTTOM = 'SportswearBottom', 'SportswearBottom'

class ClothSubType(models.Model):
    id = models.AutoField(primary_key=True)  # 명시적 기본 키 (정수형)
    name = models.CharField(
        max_length=50, 
        unique=True,  # 이름 중복 방지
    )

    def __str__(self):
        return self.name

class Cloth(models.Model):
    clothImage = models.ImageField(upload_to='clothes/', blank=False, null=False)
    type = models.CharField(max_length=10, choices=ClothType.choices)
    brand = models.CharField(max_length=255, blank=True, null=True)
    isFavorite = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owner')
    # ManyToManyField를 through 옵션으로 중간 테이블 ClothClothSubType 사용
    cloth_subtypes = models.ManyToManyField(ClothSubType, through='ClothClothSubType', related_name='clothes')

    def __str__(self):
        return f"Cloth {self.id} by {self.owner.username}"

class ClothClothSubType(models.Model):
    cloth = models.ForeignKey(Cloth, on_delete=models.CASCADE)
    clothSubType = models.ForeignKey(ClothSubType, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"Cloth {self.cloth.id} - {self.clothSubType.name}"