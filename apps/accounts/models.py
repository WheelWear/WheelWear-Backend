from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import PermissionDenied

class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_reform_provider = models.BooleanField(default=False)
    
    @property
    def age(self):
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return None
    
    def promote_to_reform_provider(self):
        """특정 조건을 만족하면 제공자로 승격"""
        self.is_reform_provider = True
        self.save()

    def save(self, *args, **kwargs):
        # is_reform_provider 값이 변경되려 할 때, 특정 메소드만 허용
        if self.pk is not None:  # 기존 유저
            original = User.objects.get(pk=self.pk).profile
            if original.is_reform_provider != self.is_reform_provider:
                raise PermissionDenied("is_reform_provider 필드는 직접 수정할 수 없습니다.")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class ReformProvider(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='reform_provider', null=True, blank=True)
    infoTitle = models.CharField(max_length=255)
    contactEmail = models.EmailField()
    advantage = models.CharField(max_length=255)
    description = models.TextField()
    reformCount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.infoTitle