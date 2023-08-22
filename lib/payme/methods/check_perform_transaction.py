from payme.serializers import (
    MerchatTransactionsModelSerializer,
    OrderModelSerializer
)
from payme.utils.get_params import get_params
from payme.utils.order_finder import Order


class CheckPerformTransaction:
    """
    CheckPerformTransaction class
    That's used to check perform transaction.

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-merchant-api/checktransaction
    """

    def __call__(self, params: dict) -> dict:
        serializer = MerchatTransactionsModelSerializer(
            data=get_params(params)
        )
        serializer.is_valid(raise_exception=True)

        order = OrderModelSerializer(
            instance=Order.objects.get(
                id=serializer.validated_data.get('order_id')
            )
        )

        response = {
            "result": {
                "allow": True,
                "detail": order.data.get("detail")
            }
        }

        if not order.data.get("detail"):
            del response["result"]["detail"]

        return None, response
