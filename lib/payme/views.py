import base64
import binascii

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from payme.utils.logging import logger

from payme.errors.exceptions import MethodNotFound
from payme.errors.exceptions import PermissionDenied
from payme.errors.exceptions import PerformTransactionDoesNotExist

from payme.methods.get_statement import GetStatement
from payme.methods.check_transaction import CheckTransaction
from payme.methods.cancel_transaction import CancelTransaction
from payme.methods.create_transaction import CreateTransaction
from payme.methods.perform_transaction import PerformTransaction
from payme.methods.check_perform_transaction import CheckPerformTransaction


class MerchantAPIView(APIView):
    """
    MerchantAPIView class provides payme call back functionality.
    """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request) -> Response:
        """
        Payme sends post request to our call back url.
        That methods are includes 5 methods
            - CheckPerformTransaction
            - CreateTransaction
            - PerformTransaction
            - CancelTransaction
            - CheckTransaction
            - GetStatement
        """
        password = request.META.get('HTTP_AUTHORIZATION')
        if self.authorize(password):
            incoming_data: dict = request.data
            incoming_method: str = incoming_data.get("method")

            logger.info("Call back data is incoming %s", incoming_data)

            try:
                paycom_method = self.get_paycom_method_by_name(
                    incoming_method=incoming_method
                )
            except ValidationError as error:
                logger.error("Validation Error occurred: %s", error)
                raise MethodNotFound() from error

            except PerformTransactionDoesNotExist as error:
                logger.error("PerformTransactionDoesNotExist Error occurred: %s", error)
                raise PerformTransactionDoesNotExist() from error

            order_id, action = paycom_method(incoming_data.get("params"))

        if isinstance(paycom_method, CreateTransaction):
            self.create_transaction(
                order_id=order_id,
                action=action,
            )

        if isinstance(paycom_method, PerformTransaction):
            self.perform_transaction(
                order_id=order_id,
                action=action,
            )

        if isinstance(paycom_method, CancelTransaction):
            self.cancel_transaction(
                order_id=order_id,
                action=action,
            )

        return Response(data=action)

    def get_paycom_method_by_name(self, incoming_method: str) -> object:
        """
        Use this static method to get the paycom method by name.
        :param incoming_method: string -> incoming method name
        """
        available_methods: dict = {
            "CheckPerformTransaction": CheckPerformTransaction,
            "CreateTransaction": CreateTransaction,
            "PerformTransaction": PerformTransaction,
            "CancelTransaction": CancelTransaction,
            "CheckTransaction": CheckTransaction,
            "GetStatement": GetStatement
        }

        try:
            merchant_method = available_methods[incoming_method]
        except Exception as error:
            error_message = "Unavailable method: %s", incoming_method
            logger.error(error_message)
            raise MethodNotFound(error_message=error_message) from error

        merchant_method = merchant_method()

        return merchant_method

    @staticmethod
    def authorize(password: str) -> None:
        """
        Authorize the Merchant.
        :param password: string -> Merchant authorization password
        """
        is_payme: bool = False
        error_message: str = ""

        if not isinstance(password, str):
            error_message = "Request from an unauthorized source!"
            logger.error(error_message)
            raise PermissionDenied(error_message=error_message)

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError) as error:
            error_message = "Error when authorize request to merchant!"
            logger.error(error_message)

            raise PermissionDenied(error_message=error_message) from error

        merchant_key = password.split(':')[-1]

        if merchant_key == settings.PAYME.get('PAYME_KEY'):
            is_payme = True

        if merchant_key != settings.PAYME.get('PAYME_KEY'):
            logger.error("Invalid key in request!")

        if is_payme is False:
            raise PermissionDenied(
                error_message="Unavailable data for unauthorized users!"
            )

        return is_payme

    def create_transaction(self, order_id, action) -> None:
        """
        need implement in your view class
        """
        pass

    def perform_transaction(self, order_id, action) -> None:
        """
        need implement in your view class
        """
        pass

    def cancel_transaction(self,order_id, action) -> None:
        """
        need implement in your view class
        """
        pass
