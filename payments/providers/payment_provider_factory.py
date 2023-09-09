from paymobprovider.provider import PaymobProvider


class PaymentProviderFactory:
    providers = {
        'paymob': PaymobProvider
    }

    @classmethod
    def get_payment_provider(cls, name, transaction):
        return cls.providers.get(name, 'paymob')(name, transaction)
