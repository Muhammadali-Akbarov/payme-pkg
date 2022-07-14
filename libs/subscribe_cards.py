import json
import requests


class PaymeSubscribeCards:
    __CACHE_CONTROL = "no-cache"

    def __init__(self, base_url: str, paycom_id: str) -> None:
        self.__base_url: str = base_url
        self.__paycom_id: str = paycom_id

        self.__headers: dict = {
            "X-Auth": self.__paycom_id,
            "Cache-Control": self.__CACHE_CONTROL,
        }
        self.__methods: dict = {
            "cards_check": "cards.check",
            "cards_create": "cards.create",
            "cards_remove": "cards.remove",
            "cards_verify": "cards.verify",
            "receipts_get_all": "receipts.get_all",
            "cards_get_verify_code": "cards.get_verify_code",
        }

    def __request(self, card_info: dict) -> dict:
        context: dict = {
            "data": card_info,
            "url": self.__base_url,
            "headers": self.__headers,
        }
        return requests.post(**context).json()

    def _cards_create(self, id: str, number: str, expire: str, save: bool) -> dict:
        """Создание токена пластиковой карты"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('cards_create'),
            "params": {
                "card": {
                    "number": number,
                    "expire": expire,
                },
                "save": save,
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _card_get_verify_code(self, id: int, token: str) -> dict:
        """Запрос кода для верификации карты"""
        context: dict = {
            "id": id,
            "method": self.__methods.get('cards_get_verify_code'),
            "params": {
                "token": token,
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _cards_verify(self, id: int, verify_code: int, token: str) -> dict:
        """Верификация карты с помощью кода отправленного по СМС."""
        context: dict = {
            "id": id,
            "method": self.__methods.get("cards_verify"),
            "params": {
                "token": token,
                "code": verify_code
            }
        }
        return self.__request(self._parse_to_json(**context))

    def _cards_check(self, id: int, token: str) -> dict:
        """Проверка токена карты"""
        context: dict = {
            "id": id,
            "method": self.__methods.get("cards_check"),
            "params": {
                "token": token,
            }
        }

        return self.__request(self._parse_to_json(**context))

    def _cards_remove(self, id: int, token: str) -> dict:
        """Удаление токена карты"""
        context: dict = {
            "id": id,
            "method": self.__methods.get("cards_remove"),
            "params": {
                "token": token,
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


payme_subscribe_cards = PaymeSubscribeCards(
    base_url="payme_base_url",
    paycom_id="your_paycom_id_from_payme",
)
