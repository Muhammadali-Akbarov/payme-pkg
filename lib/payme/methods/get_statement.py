from django.db import DatabaseError

from payme.utils.logging import logger
from payme.models import MerchatTransactionsModel
from payme.serializers import MerchatTransactionsModelSerializer as MTMS
from payme.utils.make_aware_datetime import make_aware_datetime as mad


class GetStatement:
    """
    GetStatement class
    Transaction information is used for reconciliation
    of merchant and Payme Business transactions.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/getstatement
    """

    def __call__(self, params: dict):
        clean_data: dict = MTMS.get_validated_data(
            params=params
        )

        start_date, end_date = mad(
            int(clean_data.get("start_date")),
            int(clean_data.get("end_date"))
        )

        try:
            transactions = \
                MerchatTransactionsModel.objects.filter(
                    created_at__gte=start_date,
                    created_at__lte=end_date
                )

            if not transactions:  # no transactions found for the period
                return {"result": {"transactions": []}}

            statements = [
                {
                    'id': t._id,
                    'time': int(t.created_at.timestamp()),
                    'amount': t.amount,
                    'account': {'order_id': t.order_id},
                    'create_time': t.state,
                    'perform_time': t.perform_time,
                    'cancel_time': t.cancel_time,
                    'transaction': t.order_id,
                    'state': t.state,
                    'reason': t.reason,
                    'receivers': []  # not implemented
                } for t in transactions
            ]

            response: dict = {
                "result": {
                    "transactions": statements
                }
            }
        except DatabaseError as error:
            logger.error("Error getting transaction in database: %s", error)
            response = {"result": {"transactions": []}}

        return None, response
