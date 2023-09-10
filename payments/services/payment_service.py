from rest_framework.request import Request

from orders.exceptions import NoCurrentOrderException
from payments.models import PaymentTransaction
from payments.providers import PaymentProviderAbstract
from payments.providers.payment_provider_factory import PaymentProviderFactory


class PaymentService:
    provider: PaymentProviderAbstract = None
    provider_name: str = ""

    provider_url: str = ""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    def start_payment_session(self, request):
        user_order = request.user.cart.current_order
        if not user_order:
            raise NoCurrentOrderException()
        payment_transaction = PaymentTransaction.objects.create(
            order=user_order,
            amount=user_order.get_total_amount_for_payment(),
            provider_name=self.provider_name
        )
        self.provider = PaymentProviderFactory.get_payment_provider(self.provider_name, payment_transaction)

        self.provider_url = self.provider.get_payment_session_url()

    def get_payment_session_link(self) -> str:
        return self.provider_url

    def close_payment_session(self, request: Request):
        self.provider = PaymentProviderFactory.get_payment_provider(self.provider_name)
        self.provider.parse_webhook_response(request.data, hmac=request.query_params.get('hmac'))

        if self.provider.is_payment_done():
            self.provider.get_payment_transaction().confirm_payment()
        else:
            self.provider.get_payment_transaction().notify_user_with_failed_payment_transaction()
