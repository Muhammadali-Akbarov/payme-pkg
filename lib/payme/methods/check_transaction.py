from payme.utils.logger import logged
from payme.utils.get_params import get_params

from payme.models import MerchatTransactionsModel
from payme.serializers import MerchatTransactionsModelSerializer


class CheckTransaction:
    def __call__(self, params: dict) -> None:
        response: dict = None
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data: dict = serializer.validated_data

        try:
            logged_message = "started check transaction in db"
            transaction = \
                MerchatTransactionsModel.objects.get(
                    _id=clean_data.get("_id"),
                )
            logged(
                logged_message=logged_message,
                logged_type="info",
            )
            response = {
                "result": {
                    "create_time": int(transaction.created_at_ms),
                    "perform_time": transaction.perform_time,
                    "cancel_time": transaction.cancel_time,
                    "transaction": transaction.transaction_id,
                    "state": transaction.state,
                    "reason": None,
                }
            }
            if transaction.reason is not None:
                response["result"]["reason"] = int(transaction.reason)

        except Exception as e:
            logged_message = "error during get transaction in db {}{}"
            logged(
                logged_message=logged_message.format(e, clean_data.get("id")),
                logged_type="error",
            )

        return response
