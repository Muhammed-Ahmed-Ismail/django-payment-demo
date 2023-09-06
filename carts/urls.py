from rest_framework import routers
from .views import CartLineViewSet, CartViewSet

router = routers.SimpleRouter()
router.register('cart_lines', CartLineViewSet)
router.register('', CartViewSet)

urlpatterns = router.urls
