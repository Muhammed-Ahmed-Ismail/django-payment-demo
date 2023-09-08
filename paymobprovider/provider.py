import os
import requests
import json

from payments.models import PaymentTransaction
from payments.providers.payment_provider_abc import PaymentProviderAbstract
from paymobprovider.exceptions import ProviderException


class PaymobProvider(PaymentProviderAbstract):
    auth_token: str = ""
    payment_auth_token: str = ""
    payment_transaction: PaymentTransaction
    order_id: int = None

    def __init__(self, name, payment_transaction):
        super().__init__(name)
        self.payment_transaction = payment_transaction

    def get_payment_session_url(self, request) -> str:
        paymob_iframe_id = os.environ.get('PAYMOB_IFRAME_ID')
        self.run_paymob_card_payment_flow()
        return f'https://accept.paymobsolutions.com/api/acceptance/iframes/{paymob_iframe_id}?payment_token={self.payment_auth_token}'

    def run_paymob_card_payment_flow(self):
        self.get_paymob_auth_token()
        self.register_paymob_order()
        self.request_payment_key()

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

        user = self.payment_transaction.user
        payment_key_req_payload = {
            "auth_token": self.auth_token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": self.order_id,
            "billing_data": {
                "email": user.email,
                "first_name": user.first_name or 'FOO',
                "street": user.profile.address or 'FOO',
                "last_name": user.last_name,
                "integration_id": os.environ.get('PAYMOB_INTEGRATION_ID'),
                "apartment": "NA",
                "floor": "NA",
                "building": "NA",
                "phone_number": "NA",
                "shipping_method": "NA",
                "postal_code": "NA",
                "city": "NA",
                "country": "NA",
                "state": "NA"
            },
            "currency": "EGP",
            "lock_order_when_paid": "false"
        }

        try:
            payment_key_response = requests.post(payment_key_url, json=payment_key_req_payload,
                                                 timeout=os.environ.get('TIMEOUT'))
        except requests.exceptions.Timeout:
            raise ProviderException('Time out')
        if payment_key_response.status_code != 200:
            raise ProviderException()

        payment_url_token = json.loads(payment_key_response.text)['token']

        self.payment_auth_token = payment_url_token
