import time

from payme.utils.get_params import get_params

from payme.utils.logger import logged
from payme.models import MerchatTransactionsModel
from payme.serializers import MerchatTransactionsModelSerializer


class PerformTransaction:
    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data: dict = serializer.validated_data
        response: dict = None
        try:
            logged_message = "started check trx in db(perform_transaction)"
            transaction = \
                MerchatTransactionsModel.objects.get(
                    _id=clean_data.get("_id"),
                )
            logged(
                logged_message=logged_message,
                logged_type="info",
            )
            transaction.state = 2
            if transaction.perform_time == 0:
                transaction.perform_time = int(time.time() * 1000)

            transaction.save()
            response: dict = {
                "result": {
                    "perform_time": int(transaction.perform_time),
                    "transaction": transaction.transaction_id,
                    "state": int(transaction.state),
                }
            }
        except Exception as e:
            logged_message = "error during get transaction in db {}{}"
            logged(
                logged_message=logged_message.format(e, clean_data.get("id")),
                logged_type="error",
            )

        return response
