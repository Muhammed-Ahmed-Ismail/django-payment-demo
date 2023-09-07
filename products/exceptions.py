from rest_framework.exceptions import APIException


class ProductOutOfStock(APIException):
    status_code = 400
    default_detail = "Product out of stock"
    default_code = "Out of stock"
