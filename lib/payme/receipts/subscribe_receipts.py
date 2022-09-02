import json
import requests


class PaymeSubscribeReceipts:
    """The PaymeSubscribeReceipts class inclues
    all paycom methods which are belongs receipts part.

    :param base_url string: The base url of the paycom api
    :param paycom_id string: The paycom_id uses to identify
    :param paycom_key string: The paycom_key uses to identify too
    """
    __P2P_DESCRIPTION = "P2P Transaction"

    def __init__(self, base_url: str, paycom_id: str, paycom_key: str) -> None:
        self.__base_url: str = base_url
        self.__headers: dict = {
            "X-Auth": f"{paycom_id}:{paycom_key}"
        }
        self.__methods: dict = {
            "receipts_get": "receipts.get",
            "receipts_pay": "receipts.pay",
            "receipts_send": "receipts.send",
            "receipts_check": "receipts.check",
            "receipts_cancel": "receipts.cancel",
            "receipts_create": "receipts.create",
            "receipts_create_p2p": "receipts.p2p",
            "receipts_get_all": "receipts.get_all",
        }

    def __request(self, data: dict) -> dict:
        req_data: dict = {
            "data": data,
            "url": self.__base_url,
            "headers": self.__headers,
        }
        return requests.post(**req_data).json()

    def _receipts_create(self, amount: float, order_id: int) -> dict:
        """Use this method to create a new payment receipt.

        :param amount float: Payment amount in tiyins
        :param order_id int: Order object ID

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.create
        """
        data: dict = {
            "method": self.__methods.get("receipts_create"),
            "params": {
                "amount": amount,
                "account": {
                    "order_id": order_id,
                }
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _receipts_create_p2p(self, token: str, amount: float) -> dict:
        """Use this method to create a new P2P Transactionm,
        It works only production mode not test mode.

        :param token string: The card's active token
        :param amount float: The amount for person to person transaction
        """
        data: dict = {
            "method": self.__methods.get("receipts_create_p2p"),
            "params": {
                "token": token,
                "amount": amount,
                "description": self.__P2P_DESCRIPTION
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _receipts_pay(self, invoice_id: str, token: str, phone: str) -> dict:
        """Use this method to pay for an exist receipt.

        :param invoice_id: invoice id for indentity transaction
        :param token string: The card's active token
        :param phone string: The payer's phone number

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.pay
        """
        data: dict = {
            "method": self.__methods.get("receipts_pay"),
            "params": {
                "id": invoice_id,
                "token": token,
                "payer": {
                    "phone": phone,
                }
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _receipts_send(self, invoice_id: str, phone: str) -> dict:
        """Use this method to send a receipt for payment in an SMS message.

        :param invoice_id: The invoice id for indentity transaction
        :param phone string: The payer's phone number

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.send
        """
        data: dict = {
            "method": self.__methods.get('receipts_send'),
            "params": {
                "id": invoice_id,
                "phone": phone
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _receipts_cancel(self, invoice_id: str) -> dict:
        """Use this method a paid check in the queue for cancellation.

        :param invoice_id string: The invoice id for indentity transaction

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.cancel
        """
        data: dict = {
            "method": self.__methods.get('receipts_cancel'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**data))

    def _receipts_check(self, invoice_id: str) -> dict:
        """Use this method check for an exist receipt.

        :param invoice_id string: The invoice id for indentity transaction

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.check
        """
        data: dict = {
            "method": self.__methods.get('receipts_check'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**data))

    def _reciepts_get(self, invoice_id: str) -> dict:
        """Use this method check status for an exist receipt.

        :param invoice_id string: The invoice id for indentity transaction

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.get
        """
        data: dict = {
            "method": self.__methods.get('receipts_get'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**data))

    def _reciepts_get_all(self, count: int, _from: int, to: int, offset: int) -> dict:
        """Use this method get all complete information,
        on checks for a certain period.

        :param count int: The number of checks. Maximum value - 50
        :param _from string: The date of the beginning
        :param to string: The date of the ending
        :param offset string: The number of subsequent skipped checks.

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/receipts.get_all
        """
        data: str = {
            "method": self.__methods.get('receipts_get_all'),
            "params": {
                "count": count,
                "from": _from,
                "to": to,
                "offset": offset
            }
        }
        return self.__request(self._parse_to_json(**data))

    @staticmethod
    def _parse_to_json(**kwargs) -> dict:
        """Use this static method to data dumps.
        """
        data: dict = {
            "method": kwargs.pop("method"),
            "params": kwargs.pop("params"),
        }

        return json.dumps(data)
