from django.urls import path

from rest_framework import routers

from .views import OrderViewSet, check_out

router = routers.SimpleRouter()
router.register('', OrderViewSet)
urlpatterns = router.urls + [
    path('check_out', check_out)
]
