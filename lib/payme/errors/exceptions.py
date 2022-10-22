from rest_framework.exceptions import APIException


class BasePaymeException(APIException):
    status_code = 200
    error_code = None
    message = None

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
    status_code = 200
    error_code = -32504
    message = "Permission denied"


class MethodNotFound(BasePaymeException):
    status_code = 405
    error_code = -32601
    message = 'Method not found'


class TooManyRequests(BasePaymeException):
    status_code = 200
    error_code = -31099
    message = {
        "uz": "Buyurtma tolovni amalga oshirish jarayonida",
        "ru": "Транзакция в очереди",
        "en": "Order payment status is queued"
    }


class IncorrectAmount(BasePaymeException):
    status_code = 200
    error_code = -31001
    message = {
        'ru': 'Неверная сумма',
        'uz': 'Incorrect amount',
        'en': 'Incorrect amount',
    }


class PerformTransactionDoesNotExist(BasePaymeException):
    status_code = 200
    error_code = -31050
    message = {
        "uz": "Buyurtma topilmadi",
        "ru": "Заказ не существует",
        "en": "Order does not exists"
    }
