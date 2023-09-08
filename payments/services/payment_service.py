from payments.providers import PaymentProviderAbstract


class PaymentService:
    provider: PaymentProviderAbstract = None
    provider_name: str = ""

    def __init__(self, provider_name: str):
        self.provider_name = provider_name

    def start_payment_session(self, request):
        return self.provider.get_payment_session_url(request)

    def get_payment_session_link(self) -> str:
        return self.provider.get_payment_session_url()

    def close_payment_session(self, request):
        pass
