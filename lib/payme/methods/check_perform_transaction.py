from payme.utils.get_params import get_params
from payme.serializers import MerchatTransactionsModelSerializer


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

        response = {
            "result": {
                "allow": True,
                }
            }

        return None, response
