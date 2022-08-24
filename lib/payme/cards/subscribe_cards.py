import json
import requests


class PaymeSubscribeCards:
    """The PaymeSubscribeCards class inclues
    all paycom methods which are belongs to cards.

    :param base_url string: The base url of the paycom api
    :param paycom_id string: The paycom_id uses to identify
    """
    def __init__(self, base_url: str, paycom_id: str) -> None:
        self.__base_url: str = base_url
        self.__paycom_id: str = paycom_id

        self.__headers: dict = {
            "X-Auth": self.__paycom_id,
        }
        self.__methods: dict = {
            "cards_check": "cards.check",
            "cards_create": "cards.create",
            "cards_remove": "cards.remove",
            "cards_verify": "cards.verify",
            "cards_get_verify_code": "cards.get_verify_code",
        }

    def __request(self, card_info: dict) -> dict:
        """Use this private method to request.On success,
        response will be OK with format JSON.

        :param card_info dict: Includes card data information.
        """
        req_data: dict = {
            "data": card_info,
            "url": self.__base_url,
            "headers": self.__headers,
        }

        return requests.post(**req_data).json()

    def _cards_create(self, number: str, expire: str, save: bool) -> dict:
        """Use this method to create a new card's token.

        :param number string: The card number maximum length 18 char
        :param expire string: The card expiration string maximum length 5 char
        :param save bool: Type of token

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/cards.create
        """
        data: dict = {
            "method": self.__methods.get("cards_create"),
            "params": {
                "card": {
                    "number": number,
                    "expire": expire,
                },
                "save": save,
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _card_get_verify_code(self, token: str) -> dict:
        """Use this method to get the verification code.

        :param token string: The card's non-active token

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/cards.get_verify_code
        """
        data: dict = {
            "method": self.__methods.get('cards_get_verify_code'),
            "params": {
                "token": token,
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _cards_verify(self, verify_code: int, token: str) -> dict:
        """Verification of the card using the code sent via SMS.

        :param verify_code string: Code for verification
        :param token string: The card's non-active token

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/cards.verify
        """
        data: dict = {
            "method": self.__methods.get("cards_verify"),
            "params": {
                "token": token,
                "code": verify_code
            }
        }
        return self.__request(self._parse_to_json(**data))

    def _cards_check(self, token: str) -> dict:
        """Checking the card token active or non-active.

        :param token: The card's token for checking

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/cards.check
        """
        data: dict = {
            "method": self.__methods.get("cards_check"),
            "params": {
                "token": token,
            }
        }

        return self.__request(self._parse_to_json(**data))

    def _cards_remove(self, token: str) -> dict:
        """Delete card's token on success returns success.

        :param token: The card's token for deleting

        Full method documentation:
        https://developer.help.paycom.uz/uz/metody-subscribe-api/cards.remove
        """
        data: dict = {
            "method": self.__methods.get("cards_remove"),
            "params": {
                "token": token,
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
