from django.db import models

from django_extensions.db.models import TimeStampedModel

from .order import Order

from products.models import Product


class OrderLine(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()
