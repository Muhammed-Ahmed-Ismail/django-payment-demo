import logging

_logger = logging.getLogger(__name__)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response

from payments.services import PaymentService


@api_view(['POST'])
@permission_classes([])
def paymob_webhook(request: Request):
    payment_service: PaymentService = PaymentService('paymob')
    payment_service.close_payment_session(request)
    return Response()


@api_view(['GET'])
@permission_classes([])
def paymob_transaction_response_callback(request: Request):
    return Response()
