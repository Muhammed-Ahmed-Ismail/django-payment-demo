from rest_framework import exceptions


class OrderCreationException(Exception):
    pass


class NoCurrentOrderException(exceptions.APIException):
    status_code = 400
    default_detail = "This cart has no current Order"


class MultiplePendingOrderException(exceptions.APIException):
    status_code = 400
    default_detail = "User cannot have more than one pending order"
