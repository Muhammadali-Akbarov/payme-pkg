from django.conf import settings

from rest_framework import serializers

from payme.models import Order
from payme.models import MerchatTransactionsModel
from payme.errors.exceptions import IncorrectAmount
from payme.errors.exceptions import PerformTransactionDoesNotExist


class MerchatTransactionsModelSerializer(serializers.ModelSerializer):

    class Meta:
        model: MerchatTransactionsModel = MerchatTransactionsModel
        fields: str = "__all__"

    def validate(self, data):
        """
        Validate the data given to the MerchatTransactionsModel.
        """
        if data.get("order_id") is not None:
            try:
                order = Order.objects.get(
                    id=data['order_id']
                )
                if order.amount != int(data['amount']):
                    raise IncorrectAmount()

            except IncorrectAmount:
                raise IncorrectAmount()

        return data

    def validate_amount(self, amount) -> int:
        """
        Validator for Transactions Amount
        """
        if amount is not None:
            if int(amount) <= settings.PAYME.get("PAYME_MIN_AMOUNT"):
                raise IncorrectAmount()

        return amount

    def validate_order_id(self, order_id) -> int:
        """
        Use this method to check if a transaction is allowed to be executed.
        :param order_id: string -> Order Indentation.
        """
        try:
            Order.objects.get(
                id=order_id,
            )
        except Order.DoesNotExist:
            raise PerformTransactionDoesNotExist()

        return order_id
