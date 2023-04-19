from rest_framework.exceptions import APIException


class BasePaymeException(APIException):
    """
    BasePaymeException it's APIException.
    """
    status_code = 200
    error_code = None
    message = None

    # pylint: disable=super-init-not-called
    def __init__(self, error_message: str = None):
        detail: dict = {
            "error": {
                "code": self.error_code,
                "message": self.message,
                "data": error_message
            }
        }
        self.detail = detail


class PermissionDenied(BasePaymeException):
    """
    PermissionDenied APIException \
        That is raised when the client is not allowed to server.
    """
    status_code = 200
    error_code = -32504
    message = "Permission denied"


class MethodNotFound(BasePaymeException):
    """
    MethodNotFound APIException \
        That is raised when the method does not exist.
    """
    status_code = 405
    error_code = -32601
    message = 'Method not found'


class TooManyRequests(BasePaymeException):
    """
    TooManyRequests APIException \
        That is raised when the request exceeds the limit.
    """
    status_code = 200
    error_code = -31099
    message = {
        "uz": "Buyurtma tolovni amalga oshirish jarayonida",
        "ru": "Транзакция в очереди",
        "en": "Order payment status is queued"
    }


class IncorrectAmount(BasePaymeException):
    """
    IncorrectAmount APIException \
        That is raised when the amount is not incorrect.
    """
    status_code = 200
    error_code = -31001
    message = {
        'ru': 'Неверная сумма',
        'uz': 'Incorrect amount',
        'en': 'Incorrect amount',
    }


class PerformTransactionDoesNotExist(BasePaymeException):
    """
    PerformTransactionDoesNotExist APIException \
        That is raised when a transaction does not exist or deleted.
    """
    status_code = 200
    error_code = -31050
    message = {
        "uz": "Buyurtma topilmadi",
        "ru": "Заказ не существует",
        "en": "Order does not exists"
    }


class PaymeTimeoutException(Exception):
    """
    Payme timeout exception that means that payme is working slowly.
    """
