from payments.providers import PaymentProviderAbstract


class PaymentService:
    provider: PaymentProviderAbstract = None

    def __init__(self):
        pass

    def start_payment_session(self, request):
        return self.provider.get_payment_session_url(request)
