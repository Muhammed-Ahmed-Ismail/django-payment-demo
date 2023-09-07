from django.db import models
from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    current_order = models.OneToOneField('orders.order', on_delete=models.SET_NULL, null=True)

    def check_product_in_cart(self, product_id):
        return product_id in self.get_products_in_cart()

    def get_products_in_cart(self):
        cart_lines = self.cart_lines.all()
        return {cart_line.product.id for cart_line in cart_lines}

    def add_quantity_to_cart_line(self, product_id, quantity):
        cart_lines = self.cart_lines.all()
        cart_line_for_that_product = list(filter(lambda cart_line: cart_line.product.id == product_id, cart_lines))[0]
        cart_line_for_that_product.quantity += quantity
        cart_line_for_that_product.save()

    def is_empty(self):
        return len(self.cart_lines.all()) == 0

    def is_cart_has_current_order(self):
        return self.current_order is not None
