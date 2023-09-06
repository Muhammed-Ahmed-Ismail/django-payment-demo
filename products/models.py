from django_extensions.db.models import TimeStampedModel
from django.db import models
from django.core.validators import MinValueValidator
from core.models import ActivableModel


# Create your models here.

class Product(TimeStampedModel, ActivableModel):
    name = models.CharField()
    description = models.TextField()
    price = models.DecimalField(validators=[MinValueValidator(0.0)], max_digits=5, decimal_places=2)
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
