from abc import ABC, abstractmethod

from payments.models import PaymentTransaction


class PaymentProviderAbstract(ABC):
    name: str = ""

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_payment_session_url(self, request) -> str:
        pass

    @abstractmethod
    def is_payment_done(self) -> bool:
        pass

    @abstractmethod
    def get_payment_transaction(self) -> PaymentTransaction:
        pass

    @abstractmethod
    def mark_payment_transaction(self, identifier: int):
        pass
