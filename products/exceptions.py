from rest_framework import status
from rest_framework.exceptions import APIException


class ProductPriceDuplicateVariationException(APIException):
    default_detail = "Each product's price cannot have two variation option from same variation"
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class ProductPriceMissingVariationException(APIException):
    default_detail = "Each product's price must choose variation option for all variation of it"
    status_code = status.HTTP_406_NOT_ACCEPTABLE
