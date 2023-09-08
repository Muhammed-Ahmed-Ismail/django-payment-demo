import os
import requests
import json

from payments.models import PaymentTransaction
from payments.providers.payment_provider_abc import PaymentProviderAbstract
from paymobprovider.exceptions import ProviderException


class PaymobProvider(PaymentProviderAbstract):
    auth_token: str = ""
    payment_transaction: PaymentTransaction
    order_id = None

    def __init__(self, name, payment_transaction):
        super().__init__(name)
        self.payment_transaction = payment_transaction

    def get_payment_session_url(self, request) -> str:
        pass

    def is_payment_done(self) -> bool:
        pass

    def get_payment_transaction(self) -> PaymentTransaction:
        pass

    def mark_payment_transaction(self, identifier: int):
        self.payment_transaction.provider_id = identifier
        self.payment_transaction.save()

    def get_paymob_auth_token(self):
        paymob_auth_url = os.environ.get('PAYMOB_AUTH_URL')
        paymob_api_key = os.environ.get('PAYMOB_API_KEY')

        auth_token_payload = {
            "api_key": paymob_api_key
        }

        try:
            auth_token_response = requests.post(paymob_auth_url, json=auth_token_payload,
                                                timeout=os.environ.get('TIMEOUT'))
        except requests.exceptions.Timeout:
            raise ProviderException("Time out")
        if auth_token_response.status_code != 200:
            raise ProviderException("Invalid Api key")

        token = json.loads(auth_token_response.text)['token']

        self.auth_token = token

    def register_paymob_order(self):

        paymob_register_order_url = os.environ.get('PAYMOB_REGISTER_ORDER_URL')
        amount_cents = self.payment_transaction.amount * 100

        items = [
            {
                "name": order_line.product.name,
                "amount_cents": order_line.product.price * 100,
                "description": order_line.product.description,
                "quantity": order_line.quantity
            }
            for order_line in self.payment_transaction.order.order_lines
        ]

        register_order_payload = {
            "auth_token": self.auth_token,
            "delivery_needed": "false",
            "amount_cents": amount_cents,
            "currency": "EGP",
            "items": items,
        }

        try:
            register_order_response = requests.post(paymob_register_order_url, json=register_order_payload,
                                                    timeout=os.environ.get('TIMEOUT'))
        except requests.exceptions.Timeout:
            raise ProviderException("Time out")

        if register_order_response.status_code != 200:
            raise ProviderException()

        paymob_order_id = json.loads(register_order_response.text)['id']

        self.order_id = paymob_order_id

        self.mark_payment_transaction(int(paymob_order_id))

    def request_payment_key(self):
        payment_key_url = os.environ.get('PAYMOB_PAYMENT_KEY_URL')

        amount_cents = self.payment_transaction.amount * 100

        payment_key_req_payload = {
            "auth_token": self.auth_token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": self.order_id,
            "billing_data": {
                "apartment": "803",
                "email": "claudette09@exa.com",
                "floor": "42",
                "first_name": "Clifford",
                "street": "Ethan Land",
                "building": "8028",
                "phone_number": "+86(8)9135210487",
                "shipping_method": "PKG",
                "postal_code": "01898",
                "city": "Jaskolskiburgh",
                "country": "CR",
                "last_name": "Nicolas",
                "state": "Utah"
            },
            "currency": "EGP",
            "integration_id": os.environ.get('PAYMOB_INTEGRATION_ID'),
            "lock_order_when_paid": "false"
        }
