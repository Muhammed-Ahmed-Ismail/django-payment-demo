from django.urls import path

from rest_framework import routers

from .views import OrderViewSet, check_out, cancel_order

router = routers.SimpleRouter()
router.register('', OrderViewSet)
urlpatterns = router.urls + [
    path('check_out', check_out),
    path('cancel_order', cancel_order)
]
