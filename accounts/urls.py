from django.urls import path

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers

from .views import signup, ProfileViewSet

router = routers.DefaultRouter()
router.register(r'profiles', ProfileViewSet)

urlpatterns = router.urls + [
    path('signup', signup),
    path('login', obtain_auth_token)
]
