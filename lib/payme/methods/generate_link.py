import base64
import json
import os
import typing
import uuid
from dataclasses import dataclass

import websocket
from websocket import WebSocketApp

from django.conf import settings

from payme.errors.exceptions import QRCodeError

PAYME_ID = settings.PAYME.get('PAYME_ID')
PAYME_ACCOUNT = settings.PAYME.get('PAYME_ACCOUNT')
PAYME_CALL_BACK_URL = settings.PAYME.get('PAYME_CALL_BACK_URL')
PAYME_URL = settings.PAYME.get("PAYME_URL")


@dataclass
class GeneratePayLink:
    """
    GeneratePayLink dataclass
    That's used to generate pay lint for each order.

    Parameters
    ----------
    order_id: int — The order_id for paying
    amount: float — The amount belong to the order

    Returns str — pay link
    ----------------------

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/initsializatsiya-platezhey/
    """
    order_id: str
    amount: float

    def generate_link(self) -> str:
        """
        GeneratePayLink for each order.

        Full method documentation
        ----------
        https://developer.help.paycom.uz/initsializatsiya-platezhey/otpravka-cheka-po-metodu-get

        """
        generated_pay_link: str = "{payme_url}/{encode_params}"
        params: str = 'm={payme_id};ac.{payme_account}={order_id};a={amount};c={call_back_url}'

        params = params.format(
            payme_id=PAYME_ID,
            payme_account=PAYME_ACCOUNT,
            order_id=self.order_id,
            amount=self.amount,
            call_back_url=PAYME_CALL_BACK_URL
        )
        encode_params = base64.b64encode(params.encode("utf-8"))
        return generated_pay_link.format(
            payme_url=PAYME_URL,
            encode_params=str(encode_params, 'utf-8')
        )

    def __send_and_receive_data(self, data) -> typing.Union[str, None]:
        # pylint: disable=missing-function-docstring

        message = None

        def on_message(ws: WebSocketApp, _message):
            nonlocal message
            message = _message

            ws.close()

        websocket.enableTrace(False)

        ws = WebSocketApp(
            url="wss://checkout.paycom.uz/",
            keep_running=False,
            on_message=on_message
        )

        ws.on_open = lambda ws: ws.send(json.dumps(data))
        ws.run_forever(ping_interval=0.1)

        return message

    def to_qrcode(self, path: str = 'qr-codes', filename: str = None, **kwargs):
        """ 
        Generate qr-code for order.

        Full method documentation
        ----------
        https://developer.help.paycom.uz/initsializatsiya-platezhey/generatsiya-knopki-oplaty-i-qr-koda

        Parameters 
        ---------- 
        path: str -> output path (folder) name
        filename: str -> output image name without suffix
        lang: str -> user language. available values: ru, uz, en.
        callback: str -> return url after payment or payment cancellation.

        Returns
        ----------
        str -> path of qr code svg
        """
        data = {
            "lang": kwargs.get("lang", "ru"),
            "merchant": PAYME_ID,
            "amount": self.amount,
            "account": {PAYME_ACCOUNT: self.order_id},
            "callback": kwargs.get("callback", PAYME_CALL_BACK_URL)
        }
        message = self.__send_and_receive_data(data)

        if message is None:
            raise QRCodeError

        if not os.path.exists(path):
            os.makedirs(path)

        image_name = uuid.uuid4().hex if not filename else filename
        image_output_path = f'{path}/{image_name}.svg'

        with open(image_output_path, 'w', encoding='utf-8') as svg:
            svg.write(message.split(',')[-1])

        return image_output_path

    @staticmethod
    def to_tiyin(amount: float) -> float:
        """ 
        Convert from soum to tiyin. 

        Parameters 
        ---------- 
        amount: float -> order amount 
        """
        return amount * 100

    @staticmethod
    def to_soum(amount: float) -> float:
        """ 
        Convert from tiyin to soum. 

        Parameters 
        ---------- 
        amount: float -> order amount 
        """
        return amount / 100
