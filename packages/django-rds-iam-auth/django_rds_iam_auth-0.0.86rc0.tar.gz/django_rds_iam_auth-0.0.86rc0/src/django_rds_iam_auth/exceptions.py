from rest_framework.exceptions import APIException


class InvalidTokenException(APIException):
    status_code = 403
    default_detail = 'Invalid token'
    default_code = 'invalid_token'


class TokenExpiredException(APIException):
    status_code = 401
    default_detail = 'Token expired'
    default_code = 'token_expired'
