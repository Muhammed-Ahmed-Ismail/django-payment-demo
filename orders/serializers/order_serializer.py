from rest_framework import serializers

from ..models import Order

from .order_line_serializer import OrderLineSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer

    class Meta:
        model = Order
        fields = ['id', 'order_lines']
