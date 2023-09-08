from rest_framework import exceptions
from rest_framework import status


class ProviderException(exceptions.APIException):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    default_detail = "Some Error Occurred During Calling Payment Provider"
