from django.db import models

from django_extensions.db.models import TimeStampedModel
from products.models import Product
from .cart import Cart


class CartLine(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_lines')
