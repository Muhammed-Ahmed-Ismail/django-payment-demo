from django.db import models, transaction

from django_extensions.db.models import TimeStampedModel

from django.contrib.auth import get_user_model

from django.core.mail import send_mail

from carts.models import Cart

from products.models import Product
from products.exceptions import ProductOutOfStock

from .order_line import OrderLine

from ..exceptions import OrderCreationException

User = get_user_model()


class OrderStatus(models.TextChoices):
    PAID = 'paid'
    PENDING = 'pending'
    DRAFT = 'draft'
    CANCEL = 'cancel'


class Order(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')

    status = models.CharField(choices=OrderStatus.choices, default=OrderStatus.DRAFT)

    total = models.DecimalField(decimal_places=2, max_digits=10, null=True)

    def create_order_from_cart(self, cart: Cart):
        cart_lines = cart.cart_lines.all()

        products_in_cart = cart.get_products_in_cart()
        product_objects = Product.objects.select_for_update().filter(id__in=products_in_cart)
        total = 0
        try:
            with transaction.atomic():
                for product in product_objects:
                    product_cart_lines = list(filter(lambda cart_line: cart_line.product.id == product.id, cart_lines))
                    for cart_line in product_cart_lines:
                        product.quantity_in_stock -= cart_line.quantity

                        OrderLine.objects.create(
                            order=self,
                            product=product,
                            quantity=cart_line.quantity
                        )
                        total += cart_line.quantity * product.price
                        product.save()
                    if product.quantity_in_stock < 0:
                        raise OrderCreationException()
        except OrderCreationException:
            raise ProductOutOfStock()
        else:
            self.set_pending()
            self.total = total
            self.save()
            cart.current_order = self
            cart.save()

    def cancel(self, cart: Cart):
        order_lines = self.order_lines.all()
        for order_line in order_lines:
            order_line.cancel()
        cart.current_order = None
        cart.save()

    def get_total_amount_for_payment(self):
        return self.total

    def set_done(self):
        self.status = OrderStatus.PAID
        self.send_email_for_user_with_done_state()
        self.save()

    def send_email_for_user_with_done_state(self):
        message = f"""
            Dear {self.user.first_name or 'customer'},
            
            Your order with number S{self.id} done successfully!
        """

        return send_mail(subject='Order is Done', message=message, from_email="django-pay@gmail.com",
                         recipient_list=[self.user.email], fail_silently=False)

    def set_pending(self):
        self.status = OrderStatus.PENDING
        self.save()
