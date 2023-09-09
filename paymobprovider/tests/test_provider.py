from django.test import SimpleTestCase, TestCase
from paymobprovider.provider import PaymobProvider

from payments.models import PaymentTransaction
from orders.models import Order

from django.contrib.auth import get_user_model


class TestProvider(SimpleTestCase):

    def test_validate_paymob_response(self):
        response_object_sample = {'type': 'TRANSACTION',
                                  'obj': {'id': 131114314, 'pending': False, 'amount_cents': 14, 'success': True,
                                          'is_auth': False, 'is_capture': False, 'is_standalone_payment': True,
                                          'is_voided': False, 'is_refunded': False, 'is_3d_secure': True,
                                          'integration_id': 3285996, 'profile_id': 673684,
                                          'has_parent_transaction': False,
                                          'order': {'id': 149435652, 'created_at': '2023-09-09T15:12:35.622576',
                                                    'delivery_needed': False, 'merchant': {'id': 673684,
                                                                                           'created_at': '2023-01-15T13:03:23.042416',
                                                                                           'phones': ['+201112597144'],
                                                                                           'company_emails': [
                                                                                               'muhamed.ismail.objects@gmail.com'],
                                                                                           'company_name': 'objects',
                                                                                           'state': '',
                                                                                           'country': 'EGY',
                                                                                           'city': 'Cairo',
                                                                                           'postal_code': '',
                                                                                           'street': ''},
                                                    'collector': None, 'amount_cents': 14,
                                                    'shipping_data': {'id': 73449522, 'first_name': 'FOO',
                                                                      'last_name': 'FOO', 'street': 'FOO',
                                                                      'building': 'NA', 'floor': 'NA',
                                                                      'apartment': 'NA', 'city': 'NA', 'state': 'NA',
                                                                      'country': 'NA', 'email': 'admin@admin.com',
                                                                      'phone_number': 'NA', 'postal_code': 'NA',
                                                                      'extra_description': '', 'shipping_method': 'UNK',
                                                                      'order_id': 149435652, 'order': 149435652},
                                                    'currency': 'EGP', 'is_payment_locked': False, 'is_return': False,
                                                    'is_cancel': False, 'is_returned': False, 'is_canceled': False,
                                                    'merchant_order_id': None, 'wallet_notification': None,
                                                    'paid_amount_cents': 14, 'notify_user_with_email': False, 'items': [
                                                  {'name': 's', 'description': 's', 'amount_cents': 2, 'quantity': 7}],
                                                    'order_url': 'https://accept.paymob.com/standalone/?ref=i_LRR2UTVKNnFTWkgrME55VnluNTdON25mQT09X2gzbFdNS3VEeTZqZjRaNUhRUFlJYWc9PQ',
                                                    'commission_fees': 0, 'delivery_fees_cents': 0,
                                                    'delivery_vat_cents': 0, 'payment_method': 'tbc',
                                                    'merchant_staff_tag': None, 'api_source': 'OTHER', 'data': {}},
                                          'created_at': '2023-09-09T15:12:46.608718',
                                          'transaction_processed_callback_responses': [], 'currency': 'EGP',
                                          'source_data': {'pan': '2346', 'type': 'card', 'tenure': None,
                                                          'sub_type': 'MasterCard'}, 'api_source': 'IFRAME',
                                          'terminal_id': None, 'merchant_commission': 0, 'installment': None,
                                          'discount_details': [], 'is_void': False, 'is_refund': False,
                                          'data': {'gateway_integration_pk': 3285996, 'klass': 'MigsPayment',
                                                   'created_at': '2023-09-09T12:13:00.197181',
                                                   'amount': 14.000000000000002, 'currency': 'EGP',
                                                   'migs_order': {'acceptPartialAmount': False, 'amount': 0.14,
                                                                  'creationTime': '2023-09-09T12:12:59.684Z',
                                                                  'currency': 'EGP', 'id': '149435652',
                                                                  'status': 'CAPTURED', 'totalAuthorizedAmount': 0.14,
                                                                  'totalCapturedAmount': 0.14,
                                                                  'totalRefundedAmount': 0.0}, 'merchant': 'TEST770000',
                                                   'migs_result': 'SUCCESS', 'migs_transaction': {
                                                  'acquirer': {'batch': 20230909, 'date': '0909', 'id': 'CIB_S2I',
                                                               'merchantId': '770000', 'settlementDate': '2023-09-09',
                                                               'timeZone': '+0300', 'transactionId': '123456789'},
                                                  'amount': 0.14, 'authorizationCode': '242406', 'currency': 'EGP',
                                                  'frequency': 'SINGLE', 'id': '131114314', 'receipt': '325212242406',
                                                  'source': 'INTERNET', 'terminal': 'CIBS2I05', 'type': 'PAYMENT'},
                                                   'txn_response_code': 'APPROVED', 'acq_response_code': '00',
                                                   'message': 'Approved', 'merchant_txn_ref': '131114314',
                                                   'order_info': '149435652', 'receipt_no': '325212242406',
                                                   'transaction_no': '123456789', 'batch_no': 20230909,
                                                   'authorize_id': '242406', 'card_type': 'MASTERCARD',
                                                   'card_num': '512345xxxxxx2346', 'secure_hash': '',
                                                   'avs_result_code': '', 'avs_acq_response_code': '00',
                                                   'captured_amount': 0.14, 'authorised_amount': 0.14,
                                                   'refunded_amount': 0.0, 'acs_eci': ''}, 'is_hidden': False,
                                          'payment_key_claims': {'exp': 1694265157, 'extra': {},
                                                                 'pmk_ip': '154.180.77.226', 'user_id': 1142673,
                                                                 'currency': 'EGP', 'order_id': 149435652,
                                                                 'amount_cents': 14, 'billing_data': {'city': 'NA',
                                                                                                      'email': 'admin@admin.com',
                                                                                                      'floor': 'NA',
                                                                                                      'state': 'NA',
                                                                                                      'street': 'FOO',
                                                                                                      'country': 'NA',
                                                                                                      'building': 'NA',
                                                                                                      'apartment': 'NA',
                                                                                                      'last_name': 'FOO',
                                                                                                      'first_name': 'FOO',
                                                                                                      'postal_code': 'NA',
                                                                                                      'phone_number': 'NA',
                                                                                                      'extra_description': 'NA'},
                                                                 'integration_id': 3285996,
                                                                 'lock_order_when_paid': False,
                                                                 'single_payment_attempt': False},
                                          'error_occured': False, 'is_live': False, 'other_endpoint_reference': None,
                                          'refunded_amount_cents': 0, 'source_id': -1, 'is_captured': False,
                                          'captured_amount': 0, 'merchant_staff_tag': None,
                                          'updated_at': '2023-09-09T15:13:00.482245', 'is_settled': False,
                                          'bill_balanced': False, 'is_bill': False, 'owner': 1142673,
                                          'parent_transaction': None}, 'issuer_bank': None,
                                  'transaction_processed_callback_responses': ''}
        correct_hmac_sample = '5bf943235fed1b441731300c926c3112619d329c6888656fd4f27332f22c4801e5c4f3eea2ad34ff3c45a468ad115f887ac96134bf6f069bd622e131fb2033bd'
        assert PaymobProvider.validate_paymob_response(response_object_sample,
                                                       received_hmac=correct_hmac_sample) == True


class test_payment_transaction(TestCase):
    def setUp(self) -> None:
        user = get_user_model().objects.create(
            username='test',
            password='123'
        )
        order = Order.objects.create(
            user=user
        )
        transaction = PaymentTransaction.objects.create(
            order=order,
            amount=10.99,
            provider_id=1002,
            provider_name='paymob'
        )

        self.provider = PaymobProvider('paymob', transaction)
        self.provider.payment_transaction_identifier = 1002

    def test_get_payment_transaction(self):
        assert self.provider.get_payment_transaction() is not None
