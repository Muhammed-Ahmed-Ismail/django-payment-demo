from rest_framework import serializers

from ..models import Order

from .order_line_serializer import OrderLineSerializer


class OrderSerializer(serializers.ModelSerializer):
    order_lines = OrderLineSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'order_lines']
        extra_kwargs = {
            'status': {'read_only': True}
        }
