from django.urls import path

from paymobprovider.views import paymob_webhook, paymob_transaction_response_callback

urlpatterns = [
    path('api/acceptance/post_pay', paymob_webhook),
    path('api/acceptance/transaction_response', paymob_transaction_response_callback),
]
