from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, action

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
def confirm_order(request):
    pass
