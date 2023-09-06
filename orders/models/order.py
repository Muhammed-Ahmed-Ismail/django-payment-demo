from django.db import models

from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

from carts.models import Cart

User = get_user_model()


class OrderStatus(models.TextChoices):
    PAID = 'paid'
    PENDING = 'pending'


class Order(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def create_order_from_cart(self, cart: Cart):
        pass
