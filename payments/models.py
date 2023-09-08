from django.db import models
from django_extensions.db.models import TimeStampedModel


class PaymentTransactionStatus(models.TextChoices):
    DRAFT = 'draft'
    PENDING = 'pending'
    DONE = 'done'


class PaymentTransaction(TimeStampedModel):
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payment_tran')
    status = models.CharField(choices=PaymentTransactionStatus.choices, default=PaymentTransactionStatus.DRAFT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    provider_name = models.CharField(null=True)
    provider_id = models.BigIntegerField(null=True)

    def confirm_payment(self):
        pass

    @property
    def user(self):
        return self.order.user
