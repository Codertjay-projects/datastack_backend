from rest_framework.exceptions import (
    APIException,
    ParseError,
    PermissionDenied,
    AuthenticationFailed,
)
from .message import (
    NOT_ACCEPTABLE_REQUEST,
    EMAIL_NOT_VERIFIED,
    EMAIL_OTP_2FA,
    SERVER_ERROR,
)


# When request is invalid
class NotAcceptable(APIException):
    status_code = 406
    default_details = NOT_ACCEPTABLE_REQUEST
    default_code = NOT_ACCEPTABLE_REQUEST


# Exception for the codndition if email is not verfied by user
class EmailNotVerified(APIException):
    status_code = 422
    default_details = EMAIL_NOT_VERIFIED
    default_code = "email_not_verfied"


# Exception for TWO-FACTOR enabled
class TwoFactorEnabled(APIException):
    status_code = 422
    default_details = EMAIL_OTP_2FA
    default_code = "two_factor_enabled"


# Server Error
class ServerError(APIException):
    status_code = 500
    default_details = SERVER_ERROR
    default_code = "server_erroe"
