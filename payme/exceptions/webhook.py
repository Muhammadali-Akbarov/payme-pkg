"""
Init Payme base exception.
"""

import logging
import typing as t

from rest_framework import status
from rest_framework.exceptions import APIException

logger = logging.getLogger(__name__)

MessageT = t.Optional[t.Union[str, t.Dict[str, str]]]


class BasePaymeException(APIException):
    """
    BasePaymeException inherits from APIException.
    """

    status_code: int = status.HTTP_200_OK
    error_code: t.Optional[int] = None
    message: MessageT = None

    # pylint: disable=super-init-not-called
    def __init__(self, message: str = None):
        detail: dict = {
            "error": {"code": self.error_code, "message": self.message, "data": message}
        }
        logger.error(f"Payme error detail: {detail}")
        self.detail = detail


class PermissionDenied(BasePaymeException):
    """
    PermissionDenied APIException.

    Raised when the client is not allowed to access the server.
    """

    status_code = status.HTTP_200_OK
    error_code = -32504
    message = "Permission denied."


class InternalServiceError(BasePaymeException):
    """
    InternalServiceError APIException.

    Raised when a transaction fails to perform.
    """

    status_code = status.HTTP_200_OK
    error_code = -32400
    message = {
        "uz": "Tizimda xatolik yuzaga keldi.",
        "ru": "Внутренняя ошибка сервиса.",
        "en": "Internal service error.",
    }


class MethodNotFound(BasePaymeException):
    """
    MethodNotFound APIException.

    Raised when the requested method does not exist.
    """

    status_code = status.HTTP_405_METHOD_NOT_ALLOWED
    error_code = -32601
    message = "Method not found."


class AccountDoesNotExist(BasePaymeException):
    """
    AccountDoesNotExist APIException.

    Raised when an account does not exist or has been deleted.
    """

    status_code = status.HTTP_200_OK
    error_code = -31050
    message = {
        "uz": "Hisob topilmadi.",
        "ru": "Счет не найден.",
        "en": "Account does not exist.",
    }


class IncorrectAmount(BasePaymeException):
    """
    IncorrectAmount APIException.

    Raised when the provided amount is incorrect.
    """

    status_code = status.HTTP_200_OK
    error_code = -31001
    message = {
        "ru": "Неверная сумма.",
        "uz": "Noto'g'ri summa.",
        "en": "Incorrect amount.",
    }


class TransactionAlreadyExists(BasePaymeException):
    """
    TransactionAlreadyExists APIException.

    Raised when a transaction already exists in the system,
    preventing the creation of a new transaction with the same identifier.

    Attributes:
        status_code (int): The HTTP status code for the response.
        error_code (int): The specific error code for this exception.
        message (dict): A dictionary containing localized error messages.
    """

    status_code = status.HTTP_200_OK
    error_code = -31099
    message = {
        "uz": "Tranzaksiya allaqachon mavjud.",
        "ru": "Транзакция уже существует.",
        "en": "Transaction already exists.",
    }


class InvalidFiscalParams(BasePaymeException):
    """
    InvalidFiscalParams APIException.

    Raised when the provided fiscal parameters are invalid.
    """

    status_code = status.HTTP_200_OK
    error_code = -32602
    message = {
        "uz": "Fiskal parameterlarida kamchiliklar bor",
        "ru": "Неверные фискальные параметры.",
        "en": "Invalid fiscal parameters.",
    }


class InvalidAccount(BasePaymeException):
    """
    InvalidAccount APIException.

    Raised when the provided account is invalid.
    """

    status_code = status.HTTP_200_OK
    error_code = -32400
    message = {
        "uz": "Hisob nomida kamchilik bor",
        "ru": "Неверный номер счета.",
        "en": "Invalid account.",
    }


exception_whitelist = (
    IncorrectAmount,
    MethodNotFound,
    PermissionDenied,
    AccountDoesNotExist,
    TransactionAlreadyExists,
    InvalidFiscalParams,
    InvalidAccount,
)
