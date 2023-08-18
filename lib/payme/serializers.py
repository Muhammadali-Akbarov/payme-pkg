from django.conf import settings

from rest_framework import serializers

from payme.models import MerchatTransactionsModel
from payme.utils.get_params import get_params
from payme.utils.logging import logger
from payme.utils.order_finder import Order

from payme.errors.exceptions import (
    PerformTransactionDoesNotExist,
    IncorrectAmount
)


class MerchatTransactionsModelSerializer(serializers.ModelSerializer):
    """
    MerchatTransactionsModelSerializer class \
        That's used to serialize merchat transactions data.
    """
    start_date = serializers.IntegerField(allow_null=True)
    end_date = serializers.IntegerField(allow_null=True)

    class Meta:
        # pylint: disable=missing-class-docstring
        model: MerchatTransactionsModel = MerchatTransactionsModel
        fields: str = "__all__"
        extra_fields = ['start_date', 'end_date']

    def validate(self, attrs) -> dict:
        """
        Validate the data given to the MerchatTransactionsModel.
        """
        if attrs.get("order_id") is not None:
            try:
                order = Order.objects.get(
                    id=attrs['order_id']
                )
                if order.amount != float(attrs['amount']):
                    raise IncorrectAmount()

            except IncorrectAmount as error:
                logger.error("Invalid amount for order: %s", attrs['order_id'])
                raise IncorrectAmount() from error

        return attrs

    def validate_amount(self, amount: float) -> float:
        """
        Validator for Transactions Amount.
        """
        if amount is None:
            raise IncorrectAmount()

        if amount <= float(settings.PAYME.get("PAYME_MIN_AMOUNT", 0)):
            raise IncorrectAmount("Payment amount is less than allowed.")

        return amount

    def validate_order_id(self, order_id: int) -> int:
        """
        Use this method to check if a transaction is allowed to be executed.

        Parameters
        ----------
        order_id: str -> Order Indentation.
        """
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist as error:
            logger.error("Order does not exist order_id: %s", order_id)
            raise PerformTransactionDoesNotExist() from error

        return order_id

    @staticmethod
    def get_validated_data(params: dict) -> dict:
        """
        This static method helps to get validated data.

        Parameters
        ----------
        params: dict — Includes request params.
        """
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)
        clean_data: dict = serializer.validated_data

        return clean_data


class OrderModelSerializer(serializers.ModelSerializer):
    """
    OrderModelSerializer class \
        That's used to serialize orders detail data.
    """
    class Meta:
        # pylint: disable=missing-class-docstring
        model = Order
        depth = 2
        exclude = ["id"]
        read_only_fields = ["__all__"]

    def clean_empty(self, data):
        # pylint: disable=missing-function-docstring
        if isinstance(data, dict):
            return {
                k: v
                for k, v in ((k, self.clean_empty(v)) for k, v in data.items())
                if v is not None and k != 'id'
            }
        if isinstance(data, list):
            return [v for v in map(self.clean_empty, data) if v]

        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)

        return self.clean_empty(ret)
