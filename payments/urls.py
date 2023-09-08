from django.urls import path

from payments.views import pay

urlpatterns = [
    path('pay', pay)
]
