from rest_framework.exceptions import APIException


class NoOrderToPayFor(APIException):
    status_code = 400
    default_detail = "No order to pay"
