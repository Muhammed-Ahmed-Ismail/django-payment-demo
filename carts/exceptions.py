from rest_framework import exceptions


class EmptyCartException(exceptions.APIException):
    status_code = 400
    default_detail = "Can not perform action as it is empty"
    default_code = "empty_cart"
