from rest_framework import serializers

from ..models import CartLine

from products.models import Product


class CartLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartLine
        # exclude = ['cart']
        fields = ['id', 'product', 'quantity']
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
        return value

    def create(self, data):
        user_cart = self.context['request'].user.cart
        current_cart_line = CartLine(**data, cart=user_cart)
        current_cart_line.save()
        return current_cart_line

    def save(self, **kwargs):
        user_cart = self.context['request'].user.cart
        if user_cart.check_product_in_cart(self.initial_data['product']):
            user_cart.add_quantity_to_cart_line(self.initial_data['product'], self.initial_data['quantity'])
        else:
            self.create(self.validated_data)
