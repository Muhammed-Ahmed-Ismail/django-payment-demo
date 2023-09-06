from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
from .models import Cart,CartLine

User = get_user_model()


@receiver(post_save, sender=User)
def add_cart_to_user(*args, instance=None, created=None, **kwargs):
    if created:
        user_cart = Cart(
            user=instance
        )
        user_cart.save()

