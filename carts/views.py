from rest_framework import viewsets

from .models import CartLine, Cart

from .serizlizers import CartLineSerializer, CartSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOfCartLine, IsOwnerOfCart


class CartLineViewSet(viewsets.ModelViewSet):
    serializer_class = CartLineSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCartLine]
    queryset = CartLine.objects.all()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return CartLine.objects.filter(cart=self.request.user.cart).all()
        return CartLine.objects.all()


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCart]
    queryset = Cart.objects.all()

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Cart.objects.filter(user=self.request.user).all()
        return Cart.objects.all()
