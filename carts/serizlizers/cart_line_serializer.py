from rest_framework import serializers

from ..models import CartLine

from products.models import Product


class CartLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLine
        # exclude = ['cart']
        fields = ['id', 'product', 'quantity']

        # extra_kwargs = {
        #
        # }

    def validate(self, attrs):

        product = attrs['product'] if not self.instance or attrs.get('product') else self.instance.product

        if not product.active:
            raise serializers.ValidationError('Can not put inactive product in cart')
        quantity = attrs['quantity'] if not self.instance else self.context['request'].data.get('quantity')
        if quantity and product.quantity_in_stock < quantity:
            raise serializers.ValidationError(f'Can not handel this required quantity of {product.name}')
        return attrs

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('Can not put quantity as negative value')

    def create(self, data):
        user_cart = self.context['request'].user.cart
        current_cart_line = CartLine(**data, cart=user_cart)
        current_cart_line.save()
        return current_cart_line
