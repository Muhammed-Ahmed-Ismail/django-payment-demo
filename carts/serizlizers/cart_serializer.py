from rest_framework import serializers

from ..models import Cart

from .cart_line_serializer import CartLineSerializer


class CartSerializer(serializers.ModelSerializer):
    cart_lines = CartLineSerializer(many=True)

    class Meta:
        model = Cart

        fields = ['id', 'current_order', 'cart_lines']
