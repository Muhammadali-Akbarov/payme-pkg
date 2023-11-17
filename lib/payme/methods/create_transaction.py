import uuid
import time
import datetime

from payme.utils.logging import logger
from payme.utils.get_params import get_params
from payme.models import MerchantTransactionsModel
from payme.errors.exceptions import TooManyRequests
from payme.serializers import MerchantTransactionsModelSerializer


class CreateTransaction:
    """
    CreateTransaction class
    That's used to create transaction

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/createtransaction
    """
    def __call__(self, params: dict) -> tuple:
        serializer = MerchantTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order_id")

        try:
            transaction = MerchantTransactionsModel.objects.filter(
                order_id=order_id
            ).last()

            if transaction is not None:
                if transaction._id != serializer.validated_data.get("_id"):
                    raise TooManyRequests()

        except TooManyRequests as error:
            logger.error("Too many requests for transaction %s", error)
            raise TooManyRequests() from error

        if transaction is None:
            transaction, _ = \
                MerchantTransactionsModel.objects.get_or_create(
                    _id=serializer.validated_data.get('_id'),
                    order_id=serializer.validated_data.get('order_id'),
                    transaction_id=uuid.uuid4(),
                    amount=serializer.validated_data.get('amount'),
                    created_at_ms=int(time.time() * 1000),
                )

        if transaction:
            response: dict = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }

        return order_id, response

    @staticmethod
    def _convert_ms_to_datetime(time_ms: int) -> datetime:
        """Use this format to convert from time ms to datetime format.
        """
        readable_datetime = datetime.datetime.fromtimestamp(time_ms / 1000)

        return readable_datetime
