from django.test import TestCase

from django.contrib.auth import get_user_model

from orders.models import Order


class OrderTest(TestCase):

    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username='test',
            password='123',
            email='muhammedahmedos.alex42@gmail.com'
        )

        self.order = Order.objects.create(
            user=user
        )

    def test_send_mail(self):
        assert self.order.send_email_for_user_with_done_state() != 0
