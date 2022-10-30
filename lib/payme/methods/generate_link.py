import base64
from decimal import Decimal
from dataclasses import dataclass

from django.conf import settings

PAYME_ID = settings.PAYME.get('PAYME_ID')
PAYME_ACCOUNT = settings.PAYME.get('PAYME_ACCOUNT')
PAYME_CALL_BACK_URL = settings.PAYME.get('PAYME_CALL_BACK_URL')
PAYME_URL = settings.PAYME.get("PAYME_URL")


@dataclass
class GeneratePayLink:
    order_id: str
    amount: Decimal

    def generate_link(self) -> str:
        """
        GeneratePayLink for each order.
        """
        GENERETED_PAY_LINK: str = "{payme_url}/{encode_params}"
        PARAMS: str = 'm={payme_id};ac.{payme_account}={order_id};a={amount};c={call_back_url}'

        PARAMS = PARAMS.format(
            payme_id=PAYME_ID,
            payme_account=PAYME_ACCOUNT,
            order_id=self.order_id,
            amount=self.amount,
            call_back_url=PAYME_CALL_BACK_URL
        )
        encode_params = base64.b64encode(PARAMS.encode("utf-8"))
        return GENERETED_PAY_LINK.format(
            payme_url=PAYME_URL,
            encode_params=str(encode_params, 'utf-8')
        )
    
    @staticmethod
    def to_soum(amount: Decimal) -> Decimal:
        """
        Convert from tiyin to soum
        :param amount: Decimal -> order amount
        """
        return amount * 100
    
    @staticmethod
    def to_tiyin(amount: Decimal) -> Decimal:
        """
        Convert from som to tiyin
        :param amount: Decimal -> order amount
        """
        return amount / 100