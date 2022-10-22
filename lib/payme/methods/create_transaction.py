import uuid
import time
import datetime

from payme.utils.get_params import get_params

from payme.models import MerchatTransactionsModel
from payme.errors.exceptions import TooManyRequests
from payme.serializers import MerchatTransactionsModelSerializer


class CreateTransaction:
    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data.get("order_id")

        try:
            transaction = MerchatTransactionsModel.objects.filter(
                order_id=order_id
            ).last()

            if transaction is not None:
                if transaction._id != serializer.validated_data.get("_id"):
                    raise TooManyRequests()

        except TooManyRequests:
            raise TooManyRequests()

        if transaction is None:
            transaction, _ = \
                MerchatTransactionsModel.objects.get_or_create(
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

        return response

    @staticmethod
    def _convert_ms_to_datetime(time_ms: str) -> int:
        """Use this format to convert from time ms to datetime format.
        """
        readable_datetime = datetime.datetime.fromtimestamp(time_ms / 1000)

        return readable_datetime
