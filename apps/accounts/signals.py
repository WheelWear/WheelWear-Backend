from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .serializers import UserSerializer
from .models import Profile
from vtryon.models import BodyImage

# 생성될 때 실행
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            name=instance.first_name,
        )

# 변경 시 실행
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if not hasattr(instance, 'profile'):
        # 프로필이 없다면 새로 생성
        profile = Profile.objects.create(user=instance, name=instance.first_name)
    else:
        profile = instance.profile
        profile.name = instance.first_name
        profile.save()
        
# 변경 시와 실행 시를 합친 코드 - created를 활용하여
@receiver(post_save, sender=User)
def manage_user_profile(sender, instance, created, **kwargs):
    if created:
        BodyImage.objects.create(owner=instance)
    else:
        if not hasattr(instance, 'body_images'):
            BodyImage.objects.create(owner=instance)
        else:
            body_image = instance.body_images
            body_image.save()
