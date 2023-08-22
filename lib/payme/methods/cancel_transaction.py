import time

from django.db import transaction

from payme.utils.logging import logger
from payme.models import MerchatTransactionsModel
from payme.errors.exceptions import PerformTransactionDoesNotExist
from payme.serializers import MerchatTransactionsModelSerializer as MTMS


class CancelTransaction:
    """
    CancelTransaction class
    That is used to cancel a transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/canceltransaction
    """

    @transaction.atomic
    def __call__(self, params: dict):
        clean_data: dict = MTMS.get_validated_data(
            params=params
        )
        try:
            with transaction.atomic():
                transactions: MerchatTransactionsModel = \
                    MerchatTransactionsModel.objects.filter(
                        _id=clean_data.get('_id'),
                    ).first()
                if transactions.cancel_time == 0:
                    transactions.cancel_time = int(time.time() * 1000)
                if transactions.perform_time == 0:
                    transactions.state = -1
                if transactions.perform_time != 0:
                    transactions.state = -2
                transactions.reason = clean_data.get("reason")
                transactions.save()

        except PerformTransactionDoesNotExist as error:
            logger.error("Paycom transaction does not exist: %s", error)
            raise PerformTransactionDoesNotExist() from error

        response: dict = {
            "result": {
                "state": transactions.state,
                "cancel_time": transactions.cancel_time,
                "transaction": transactions.transaction_id,
                "reason": int(transactions.reason),
            }
        }

        return transactions.order_id, response
