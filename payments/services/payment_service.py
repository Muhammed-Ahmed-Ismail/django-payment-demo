from orders.exceptions import NoCurrentOrderException
from payments.models import PaymentTransaction
from payments.providers import PaymentProviderAbstract
from payments.providers.payment_provider_factory import PaymentProviderFactory


class PaymentService:
    provider: PaymentProviderAbstract = None
    provider_name: str = ""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    def start_payment_session(self, request):
        user_order = request.user.cart.current_order
        if not user_order:
            raise NoCurrentOrderException()
        payment_transaction = PaymentTransaction.objects.create(
            order= user_order,
            amount= user_order.get_total_amount_for_payment(),
            provider_name= self.provider_name
        )
        self.provider = PaymentProviderFactory.get_payment_provider(self.provider_name, payment_transaction)

        return self.provider.get_payment_session_url()

    def get_payment_session_link(self) -> str:
        return self.provider.get_payment_session_url()

    def close_payment_session(self, request):
        pass
