import os

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated

from payments.services import PaymentService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def pay(request: Request):
    provider = request.query_params.get('provider', os.environ.get('DEFAULT_PAYMENT_PROVIDER'))
    payment_service: PaymentService = PaymentService(provider)
    payment_service.start_payment_session(request)

    return Response(data={"payment_session_url": payment_service.get_payment_session_link()}, status=status.HTTP_200_OK)
