from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import CartLine, Cart

from .serizlizers import CartLineSerializer, CartSerializer

from .permissions import IsOwnerOfCartLine, IsOwnerOfCart
from rest_framework.decorators import api_view, permission_classes


class CartLineViewSet(viewsets.ModelViewSet):
    serializer_class = CartLineSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCartLine]
    queryset = CartLine.objects.all()
    http_method_names = ['get', 'put', 'patch', 'head', 'delete', 'options', 'trace']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return CartLine.objects.filter(cart=self.request.user.cart).all()
        return CartLine.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    cart_line_serializer = CartLineSerializer(data=request.data, context={'request': request})
    if cart_line_serializer.is_valid(raise_exception=True):
        cart_line_serializer.save()
        return Response(data=cart_line_serializer.data, status=status.HTTP_201_CREATED)
    return Response()





class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsOwnerOfCart]
    queryset = Cart.objects.all()
    http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace']

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Cart.objects.filter(user=self.request.user).all()
        return Cart.objects.all()
