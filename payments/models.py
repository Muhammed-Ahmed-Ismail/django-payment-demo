from django.db import models
from django_extensions.db.models import TimeStampedModel


class PaymentTransactionStatus(models.TextChoices):
    DRAFT = 'draft'
    PENDING = 'pending'
    DONE = 'done'


class PaymentTransaction(TimeStampedModel):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE)
    status = models.CharField(choices=PaymentTransactionStatus.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
