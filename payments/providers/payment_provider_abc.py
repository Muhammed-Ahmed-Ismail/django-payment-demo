from abc import ABC, abstractmethod


class PaymentProviderAbstract(ABC):

    @abstractmethod
    def get_payment_session_url(self, request):
        pass
