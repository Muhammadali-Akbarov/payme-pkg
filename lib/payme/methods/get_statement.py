
from datetime import datetime

from django.db import DatabaseError

from payme.utils.logging import logger
from payme.models import MerchatTransactionsModel
from payme.serializers import MerchatTransactionsModelSerializer as MTMS


class GetStatement:
    """
    GetStatement class
    Transaction information is used for reconciliation 
    of merchant and Payme Business transactions.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/getstatement
    """
    async def __call__(self, params: dict):
        clean_data: dict = MTMS.get_validated_data(
            params=params
        )

        _from = int(clean_data.get("from"))
        _to = int(clean_data.get("to"))

        try:
            transactions = \
                MerchatTransactionsModel.objects.filter(
                    date__gte=datetime.fromtimestamp(_from),
                    date__lte=datetime.fromtimestamp(_to)
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

        return response
