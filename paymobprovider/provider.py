import hashlib
import hmac
import os
import requests
import json

from payments.models import PaymentTransaction
from payments.providers.payment_provider_abc import PaymentProviderAbstract
from paymobprovider.exceptions import ProviderException, PaymobWrongHmac


class PaymobProvider(PaymentProviderAbstract):
    # sending req data
    auth_token: str = ""
    payment_auth_token: str = ""
    payment_transaction: PaymentTransaction
    order_id: int = None

    # response data
    payment_transaction_identifier = None
    is_payment_done_successfully: bool = False

    def __init__(self, name, payment_transaction=None):
        super().__init__(name)
        self.payment_transaction = payment_transaction

    def get_payment_session_url(self) -> str:
        paymob_iframe_id = os.environ.get('PAYMOB_IFRAME_ID')
        self.run_paymob_card_payment_flow()
        return f'https://accept.paymobsolutions.com/api/acceptance/iframes/{paymob_iframe_id}?payment_token={self.payment_auth_token}'

    def run_paymob_card_payment_flow(self):
        self.get_paymob_auth_token()
        self.register_paymob_order()
        self.request_payment_key()

    def is_payment_done(self) -> bool:
        return self.is_payment_done_successfully

    def parse_webhook_response(self, webhook_res, **kwargs):
        if not self.validate_paymob_response(webhook_res, kwargs.get('hmac')):
            print("sssssssssssssssss")
            raise PaymobWrongHmac()
        self.payment_transaction_identifier = webhook_res['obj']['order']['id']
        self.is_payment_done_successfully = webhook_res['obj']['success']

    def get_payment_transaction(self) -> PaymentTransaction:
        transaction = PaymentTransaction.objects.filter(provider_id=self.payment_transaction_identifier,
                                                        provider_name=self.name).first()
        if not transaction:
            raise ProviderException()

        return transaction

    @classmethod
    def validate_paymob_response(cls, paymob_response, received_hmac=None) -> bool:
        if not received_hmac:
            raise PaymobWrongHmac("missing hmac")
        paymob_hmac = os.environ.get('PAYMOB_HMAC')

        approving_keys_list = ['amount_cents', 'created_at', 'currency', 'error_occured', 'has_parent_transaction',
                               'id',
                               'integration_id', 'is_3d_secure', 'is_auth', 'is_capture', 'is_refunded',
                               'is_standalone_payment', 'is_voided', 'order.id', 'owner', 'pending', 'source_data.pan',
                               'source_data.sub_type', 'source_data.type', 'success']
        con_values = ""
        nested_objects_set = {'order.id', 'source_data.pan', 'source_data.sub_type', 'source_data.type'}

        for resp_key in approving_keys_list:
            if resp_key in nested_objects_set:
                key_split = resp_key.split('.')
                value = paymob_response['obj'][key_split[0]][key_split[1]]
                if value == True:
                    con_values += 'true'
                elif value == False:
                    con_values += 'false'
                else:
                    con_values += str(value)
            else:
                value = paymob_response['obj'][resp_key]
                if value == True:
                    con_values += 'true'
                elif value == False:
                    con_values += 'false'
                else:
                    con_values += str(value)
        msg = bytes(con_values, 'utf-8')
        key = bytes(paymob_hmac, 'utf-8')
        hashed_data = hmac.new(key, msg, hashlib.sha512)
        return hmac.compare_digest(hashed_data.hexdigest(), received_hmac)

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
                                                timeout=int(os.environ.get('TIMEOUT')))
        except requests.exceptions.Timeout:
            raise ProviderException("Time out")
        if auth_token_response.status_code != 201:
            raise ProviderException("Invalid Api key")

        token = json.loads(auth_token_response.text)['token']

        self.auth_token = token

    def register_paymob_order(self):

        paymob_register_order_url = os.environ.get('PAYMOB_REGISTER_ORDER_URL')
        amount_cents = int(self.payment_transaction.amount * 100)

        items = [
            {
                "name": order_line.product.name,
                "amount_cents": int(order_line.product.price * 100),
                "description": order_line.product.description,
                "quantity": order_line.quantity
            }
            for order_line in self.payment_transaction.order.order_lines.all()
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
                                                    timeout=int(os.environ.get('TIMEOUT')))
        except requests.exceptions.Timeout:
            raise ProviderException("Time out")

        if register_order_response.status_code != 201:
            raise ProviderException()

        paymob_order_id = json.loads(register_order_response.text)['id']

        self.order_id = paymob_order_id

        self.mark_payment_transaction(int(paymob_order_id))

    def request_payment_key(self):
        payment_key_url = os.environ.get('PAYMOB_PAYMENT_KEY_URL')
        paymob_integration_id = int(os.environ.get('PAYMOB_INTEGRATION_ID'))
        amount_cents = int(self.payment_transaction.amount * 100)

        user = self.payment_transaction.user
        payment_key_req_payload = {
            "auth_token": self.auth_token,
            "amount_cents": amount_cents,
            "expiration": 3600,
            "order_id": self.order_id,
            "billing_data": {
                "email": user.email or 'admin@admin.com',
                "first_name": user.first_name or 'FOO',
                "street": user.profile.address or 'FOO',
                "last_name": user.last_name or 'FOO',
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
            "integration_id": paymob_integration_id,
            "currency": "EGP",
            "lock_order_when_paid": "false"
        }

        try:
            payment_key_response = requests.post(payment_key_url, json=payment_key_req_payload,
                                                 timeout=int(os.environ.get('TIMEOUT')))
        except requests.exceptions.Timeout:
            raise ProviderException('Time out')
        if payment_key_response.status_code != 201:
            raise ProviderException()

        payment_url_token = json.loads(payment_key_response.text)['token']

        self.payment_auth_token = payment_url_token
