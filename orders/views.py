from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response

from rest_framework import status

from core.permissions import ReadOnly

from .permissions import IsOrderOwner
from .models import Order
from .serializers import OrderSerializer


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
    user_order = Order.objects.create(user = request.user)
    user_order.create_order_from_cart(request.user.cart)

    order_serializer = OrderSerializer(instance=user_order)

    return Response(data=order_serializer.data, status=status.HTTP_200_OK)
