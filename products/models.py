from django_extensions.db.models import TimeStampedModel
from django.db import models


# Create your models here.

class Product(TimeStampedModel):
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity_in_stock = models.IntegerField()