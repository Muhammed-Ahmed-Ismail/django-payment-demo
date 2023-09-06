from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models.profile import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(*args, instance=None, created=None, **kwargs):
    if created:
        user_profile = Profile(
            user=instance
        )
        user_profile.save()

