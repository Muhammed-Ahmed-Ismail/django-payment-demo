from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product
from .serializers import ProductSerializer

from core.permissions import ReadOnly

from core.models import ActivableModel


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated & ReadOnly]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Product.objects.filter(active=True).all()
