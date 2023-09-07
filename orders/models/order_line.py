from django.db import models

from django_extensions.db.models import TimeStampedModel

from products.models import Product


class OrderLine(TimeStampedModel):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_lines')

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField()

    def cancel(self):
        self.product.quantity_in_stock += self.quantity
        self.product.save()
