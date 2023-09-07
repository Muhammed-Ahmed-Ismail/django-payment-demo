from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from rest_framework import status

from core.permissions import ReadOnly

from carts.exceptions import EmptyCartException

from .permissions import IsOrderOwner
from .models import Order
from .serializers import OrderSerializer
from .exceptions import NoCurrentOrderException, MultiplePendingOrderException


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated & ReadOnly, IsOrderOwner]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Order.objects.filter(user=self.request.user).all()
        return Order.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_out(request):
    if request.user.cart.is_empty():
        raise EmptyCartException()
    if request.user.cart.is_cart_has_current_order():
        raise MultiplePendingOrderException()
    user_order = Order.objects.create(user=request.user)
    user_order.create_order_from_cart(request.user.cart)

    order_serializer = OrderSerializer(instance=user_order)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order(request):
    user_cart = request.user.cart
    if not user_cart.current_order:
        raise NoCurrentOrderException()
    user_cart.current_order.cancel()
    return Response(data={"message": "order canceled"})
