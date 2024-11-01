import base64
import logging
import binascii
from decimal import Decimal

from django.conf import settings
from django.utils.module_loading import import_string

from rest_framework import views
from rest_framework.response import Response

from payme import exceptions
from payme.types import response
from payme.models import PaymeTransactions
from payme.util import time_to_payme, time_to_service

logger = logging.getLogger(__name__)
AccountModel = import_string(settings.PAYME_ACCOUNT_MODEL)


def handle_exceptions(func):
    """
    Decorator to handle exceptions and raise appropriate Payme exceptions.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as exc:
            message = "Invalid parameters received."
            logger.error(f"{message}: {exc}s {exc} {args} {kwargs}")
            raise exceptions.InternalServiceError(message) from exc

        except AccountModel.DoesNotExist as exc:
            logger.error(f"Account does not exist: {exc} {args} {kwargs}")
            raise exceptions.AccountDoesNotExist(str(exc)) from exc

        except PaymeTransactions.DoesNotExist as exc:
            logger.error(f"Transaction does not exist: {exc} {args} {kwargs}")
            raise exceptions.AccountDoesNotExist(str(exc)) from exc

        except exceptions.exception_whitelist as exc:
            # No need to raise exception for exception whitelist
            raise exc
        except Exception as exc:
            logger.error(f"Unexpected error: {exc} {args} {kwargs}")
            raise exceptions.InternalServiceError(str(exc)) from exc

    return wrapper


class PaymeWebHookAPIView(views.APIView):
    """
    A webhook view for Payme.
    """
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        """
        Handle the incoming webhook request.
        """
        self.__check_authorize(request)

        payme_methods = {
            "GetStatement": self.get_statement,
            "CancelTransaction": self.cancel_transaction,
            "PerformTransaction": self.perform_transaction,
            "CreateTransaction": self.create_transaction,
            "CheckTransaction": self.check_transaction,
            "CheckPerformTransaction": self.check_perform_transaction,
        }

        try:
            method = request.data["method"]
            params = request.data["params"]
        except KeyError as exc:
            message = f"Error processing webhook: {exc}"
            raise exceptions.InternalServiceError(message) from exc

        if method in payme_methods:
            result = payme_methods[method](params)
            return Response(result)

        raise exceptions.MethodNotFound("Method not supported yet!")

    @staticmethod
    def __check_authorize(request):
        """
        Verify the integrity of the request using the merchant key.
        """
        password = request.META.get('HTTP_AUTHORIZATION')
        if not password:
            raise exceptions.PermissionDenied("Missing authentication credentials")

        password = password.split()[-1]

        try:
            password = base64.b64decode(password).decode('utf-8')
        except (binascii.Error, UnicodeDecodeError) as exc:
            raise exceptions.PermissionDenied("Decoding error in authentication credentials") from exc

        try:
            payme_key = password.split(':')[-1]
        except IndexError as exc:
            message = "Invalid merchant key format in authentication credentials"
            raise exceptions.PermissionDenied(message) from exc

        if payme_key != settings.PAYME_KEY:
            raise exceptions.PermissionDenied("Invalid merchant key specified")

    @handle_exceptions
    def fetch_account(self, params: dict):
        """
        Fetch account based on settings and params.
        """
        account_field = settings.PAYME_ACCOUNT_FIELD
        account_value = params['account'].get(account_field)
        if not account_value:
            raise exceptions.InvalidAccount("Missing account field in parameters.")

        account = AccountModel.objects.get(**{account_field: account_value})

        return account

    @handle_exceptions
    def validate_amount(self, account, amount):
        """
        Validates if the amount matches for one-time payment accounts.
        """
        if not settings.PAYME_ONE_TIME_PAYMENT:
            return True

        expected_amount = Decimal(getattr(account, settings.PAYME_AMOUNT_FIELD)) * 100
        received_amount = Decimal(amount)

        if expected_amount != received_amount:
            raise exceptions.IncorrectAmount(
                f"Invalid amount. Expected: {expected_amount}, received: {received_amount}"
            )

        return True

    @handle_exceptions
    def check_perform_transaction(self, params) -> response.CheckPerformTransaction:
        """
        Handle the pre_create_transaction action.
        """
        account = self.fetch_account(params)
        self.validate_amount(account, params.get('amount'))

        result = response.CheckPerformTransaction(allow=True)
        return result.as_resp()

    @handle_exceptions
    def create_transaction(self, params) -> response.CreateTransaction:
        """
        Handle the create_transaction action.
        """
        transaction_id = params["id"]
        amount = Decimal(params.get('amount', 0))
        account = self.fetch_account(params)

        self.validate_amount(account, amount)

        defaults = {
            "amount": amount,
            "state": PaymeTransactions.INITIATING,
            "account": account,
        }

        # Handle already existing transaction with the same ID for one-time payments
        if settings.PAYME_ONE_TIME_PAYMENT:
            # Check for an existing transaction with a different transaction_id for the given account
            if PaymeTransactions.objects.filter(account=account).exclude(transaction_id=transaction_id).exists():
                message = f"Transaction {transaction_id} already exists (Payme)."
                logger.warning(message)
                raise exceptions.TransactionAlreadyExists(message)

        transaction, _ = PaymeTransactions.objects.get_or_create(
            transaction_id=transaction_id,
            defaults=defaults
        )

        result = response.CreateTransaction(
            transaction=transaction.transaction_id,
            state=transaction.state,
            create_time=time_to_payme(transaction.created_at),
        )
        result = result.as_resp()

        # callback event
        self.handle_created_payment(params, result)

        return result

    @handle_exceptions
    def perform_transaction(self, params) -> response.PerformTransaction:
        """
        Handle the successful payment.
        """
        transaction = PaymeTransactions.get_by_transaction_id(transaction_id=params["id"])

        if transaction.is_performed():
            result = response.PerformTransaction(
                transaction=transaction.transaction_id,
                state=transaction.state,
                perform_time=time_to_payme(transaction.performed_at),
            )
            return result.as_resp()

        transaction.mark_as_performed()

        result = response.PerformTransaction(
            transaction=transaction.transaction_id,
            state=transaction.state,
            perform_time=time_to_payme(transaction.performed_at),
        )
        result = result.as_resp()

        # callback successfully event
        self.handle_successfully_payment(params, result)

        return result

    @handle_exceptions
    def check_transaction(self, params: dict) -> dict | str | response.CheckPerformTransaction:
        """
        Handle check transaction request.
        """
        transaction = PaymeTransactions.get_by_transaction_id(transaction_id=params["id"])

        result = response.CheckTransaction(
            transaction=transaction.transaction_id,
            state=transaction.state,
            reason=transaction.cancel_reason,
            create_time=time_to_payme(transaction.created_at),
            perform_time=time_to_payme(transaction.performed_at),
            cancel_time=time_to_payme(transaction.cancelled_at),
        )

        return result.as_resp()

    @handle_exceptions
    def cancel_transaction(self, params) -> response.CancelTransaction:
        """
        Handle the cancelled payment.
        """
        transaction = PaymeTransactions.get_by_transaction_id(transaction_id=params["id"])

        if transaction.is_cancelled():
            return self._cancel_response(transaction)

        if transaction.is_performed():
            transaction.mark_as_cancelled(
                cancel_reason=params["reason"],
                state=PaymeTransactions.CANCELED
            )
        elif transaction.is_created_in_payme():
            transaction.mark_as_cancelled(
                cancel_reason=params["reason"],
                state=PaymeTransactions.CANCELED_DURING_INIT
            )

        result = self._cancel_response(transaction)

        # callback cancelled transaction event
        self.handle_cancelled_payment(params, result)

        return result

    @handle_exceptions
    def get_statement(self, params) -> response.GetStatement:
        """
        Retrieves a statement of transactions.
        """
        date_range = [time_to_service(params['from']), time_to_service(params['to'])]

        transactions = PaymeTransactions.objects.filter(
            created_at__range=date_range
        ).order_by('-created_at')

        result = response.GetStatement(transactions=[])

        for transaction in transactions:
            result.transactions.append({
                "transaction": transaction.transaction_id,
                "amount": transaction.amount,
                "account": {
                    settings.PAYME_ACCOUNT_FIELD: transaction.account.id
                },
                "reason": transaction.cancel_reason,
                "state": transaction.state,
                "create_time": time_to_payme(transaction.created_at),
                "perform_time": time_to_payme(transaction.performed_at),
                "cancel_time": time_to_payme(transaction.cancelled_at),
            })

        return result.as_resp()

    def _cancel_response(self, transaction):
        """
        Helper method to generate cancel transaction response.
        """
        result = response.CancelTransaction(
            transaction=transaction.transaction_id,
            state=transaction.state,
            cancel_time=time_to_payme(transaction.cancelled_at),
        )
        return result.as_resp()

    def handle_pre_payment(self, params, result, *args, **kwargs):
        """
        Handle the pre_create_transaction action. You can override this method
        """
        print(f"Transaction pre_created for this params: {params} and pre_created_result: {result}")

    def handle_created_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction created for this params: {params} and cr_result: {result}")

    def handle_successfully_payment(self, params, result, *args, **kwargs):
        """
        Handle the successful payment. You can override this method
        """
        print(f"Transaction successfully performed for this params: {params} and performed_result: {result}")

    def handle_cancelled_payment(self, params, result, *args, **kwargs):
        """
        Handle the cancelled payment. You can override this method
        """
        print(f"Transaction cancelled for this params: {params} and cancelled_result: {result}")
