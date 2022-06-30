import json
import requests

class PaymeSubscribeReceipts:
    __CACHE_CONTROL = "no-cache"
    __CONTENT_TYPE = "application/json"
    __P2P_DESCRIPTION = "P2P Transaction"

    def __init__(self, base_url: str, paycom_id: str, paycom_key: str) -> None:
        self.__base_url: str = base_url
        self.__headers: dict = {
            "X-Auth": f"{paycom_id}:{paycom_key}",
            "Content-Type": self.__CONTENT_TYPE,
            "Cache-Control": self.__CACHE_CONTROL,
        }
        self.__methods: dict = {
            "receipts_get": "receipts.get",
            "receipts_pay": "receipts.pay",
            "receipts_send": "receipts.send",
            "receipts_check": "receipts.check",
            "receipts_cancel": "receipts.cancel",
            "receipts_create": "receipts.create",
            "receipts_create_p2p": "receipts.p2p",
        }

    def __request(self, card_info: dict) -> dict:
        context: dict = {
            "data": card_info,
            "url": self.__base_url,
            "headers": self.__headers,
        }
        return requests.post(**context).json()

    def _receipts_create(self, id: int, amount: float, order_id: int) -> dict:
        """Создание чека на оплату"""
        context: dict = {
            "id": id,
            "method": self.__methods.get("receipts_create"),
            "params": {
                "amount": amount,
                "account": {
                    "order_id": order_id,
                }
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _receipts_create_p2p(self, id: int, token: str, amount: float) -> dict:
        """P2P Transaction"""
        context: dict = {
            "id": id,
            "method": self.__methods.get("receipts_create_p2p"),
            "params": {
                "token": token,
                "amount": amount,
                "description": self.__P2P_DESCRIPTION
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _receipts_pay(self, id: int, invoice_id: str, token: str, phone: str) -> dict:
        """Оплата чека"""
        context: dict = {
            "id": id,
            "method": self.__methods.get("receipts_pay"),
            "params": {
                "id": invoice_id,
                "token": token,
                "payer": {
                    "phone": phone,
                }
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _receipts_send(self, id: int, invoice_id: str, phone: str) -> dict:
        """Метод используется для отправки чека на оплату в SMS-сообщении"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('receipts_send'),
            "params": {
                "id": invoice_id,
                "phone": phone
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _receipts_cancel(self, id: int, invoice_id: str) -> dict:
        """Установка оплаченного чека в очередь на отмену"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('receipts_cancel'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**context))

    def _receipts_check(self, id: int, invoice_id: str) -> dict:
        """Проверка статуса чека"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('receipts_check'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**context))

    def _reciepts_get(self, id: int, invoice_id: str) -> dict:
        """Проверка статуса чека"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('receipts_get'),
            "params": {
                "id": invoice_id
            }
        }

        return self.__request(self._parse_to_json(**context))

    def _reciepts_get_all(self, id:int, count: int, _from: str, to: str, offset: str) -> dict:
        """Полная информация по чекам за определенный период"""
        context: str = {
            "id": int,
            "method": self.__methods.get('receipts_get_all'),
            "params": {
                "count": count,
                "from": _from,
                "to": to,
                "offset": offset
            }
        }
        return self.__request(self._parse_to_json(**context))
    
    @staticmethod
    def _parse_to_json(**kwargs) -> dict:
        context: dict = {
            "id": kwargs.pop("id"),
            "method": kwargs.pop("method"),
            "params": kwargs.pop("params"),
        }
        return json.dumps(context)


payme_subscribe_receipts = PaymeSubscribeReceipts(
    base_url="payme_base_url",
    paycom_id="your_paycom_id_from_payme",
    paycom_key="your_paycom_key_from_payme",
)

