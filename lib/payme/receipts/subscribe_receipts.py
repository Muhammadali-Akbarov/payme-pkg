from payme.utils.to_json import to_json
from payme.decorators.decorators import payme_request



class PaymeSubscribeReceipts:
    """
    The PaymeSubscribeReceipts class inclues
    all paycom methods which are belongs receipts part.

    Parameters
    ----------
    base_url string: The base url of the paycom api
    paycom_id string: The paycom_id uses to identify
    paycom_key string: The paycom_key uses to identify too

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-subscribe-api/
    """
    def __init__(
        self,
        base_url: str,
        paycom_id: str,
        paycom_key: str,
        timeout: int = 5
    ) -> "PaymeSubscribeReceipts":
        self.base_url: str = base_url
        self.headers: dict = {
            "X-Auth": f"{paycom_id}:{paycom_key}"
        }
        self.__methods: dict = {
            "receipts_get": "receipts.get",
            "receipts_pay": "receipts.pay",
            "receipts_send": "receipts.send",
            "receipts_check": "receipts.check",
            "receipts_cancel": "receipts.cancel",
            "receipts_create": "receipts.create",
            "receipts_get_all": "receipts.get_all",
        }
        self.timeout = timeout

    @payme_request
    def __request(self, data) -> dict:
        """
        Use this private method to request.
        On success,response will be OK with format JSON.

        Parameters
        ----------
        data: dict — Includes request data.

        Returns dictionary Payme Response
        ---------------------------------
        """
        return data

    def receipts_create(self, amount: float, order_id: int) -> dict:
        """
        Use this method to create a new payment receipt.

        Parameters
        ----------
        amount: float — Payment amount in tiyins
        order_id: int — Order object ID

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.create
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
        return self.__request(to_json(**data))

    def receipts_pay(self, invoice_id: str, token: str, phone: str) -> dict:
        """
        Use this method to pay for an exist receipt.

        Parameters
        ----------
        invoice_id: str — Invoice id for indentity transaction
        token: str — The card's active token
        phone: str —The payer's phone number

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.pay
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
        return self.__request(to_json(**data))

    def receipts_send(self, invoice_id: str, phone: str) -> dict:
        """
        Use this method to send a receipt for payment in an SMS message.

        Parameters
        ----------
        invoice_id: str — The invoice id for indentity transaction
        phone: str — The payer's phone number

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.send
        """
        data: dict = {
            "method": self.__methods.get('receipts_send'),
            "params": {
                "id": invoice_id,
                "phone": phone
            }
        }
        return self.__request(to_json(**data))

    def receipts_cancel(self, invoice_id: str) -> dict:
        """
        Use this method a paid check in the queue for cancellation.

        Parameters
        ----------
        invoice_id: str — The invoice id for indentity transaction

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.cancel
        """
        data: dict = {
            "method": self.__methods.get('receipts_cancel'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(to_json(**data))

    def receipts_check(self, invoice_id: str) -> dict:
        """
        Use this method check for an exist receipt.

        Parameters
        ----------
        invoice_id: str — The invoice id for indentity transaction

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.check
        """
        data: dict = {
            "method": self.__methods.get('receipts_check'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(to_json(**data))

    def reciepts_get(self, invoice_id: str) -> dict:
        """
        Use this method check status for an exist receipt.

        Parameters
        ----------
        invoice_id: str — The invoice id for indentity transaction

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.get
        """
        data: dict = {
            "method": self.__methods.get('receipts_get'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(to_json(**data))

    def reciepts_get_all(self, count: int, _from: int, _to: int, offset: int) -> dict:
        """
        Use this method get all complete information, on checks for a certain period.

        Parameters
        ----------
        count: int — The number of checks. Maximum value - 50
        _from: str — The date of the beginning
        _to: int — The date of the ending
        offset: str — The number of subsequent skipped checks.

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/receipts.get_all
        """
        data: str = {
            "method": self.__methods.get('receipts_get_all'),
            "params": {
                "count": count,
                "from": _from,
                "to": _to,
                "offset": offset
            }
        }
        return self.__request(to_json(**data))
