from django.urls import path
from rest_framework import routers
from .views import CartLineViewSet, CartViewSet, add_to_cart

router = routers.SimpleRouter()
router.register('cart_lines', CartLineViewSet)
router.register('', CartViewSet)

urlpatterns = [
    path('add_to_cart/', add_to_cart)
] + router.urls
