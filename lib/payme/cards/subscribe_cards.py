from payme.utils.to_json import to_json
from payme.decorators.decorators import payme_request


class PaymeSubscribeCards:
    """
    The PaymeSubscribeCards class inclues
    all paycom methods which are belongs to cards.

    Parameters
    ----------
    base_url: str — The base url of the paycom api
    paycom_id: str — The paycom_id uses to identify
    timeout: int — How many seconds to wait for the server to send data

    Full method documentation
    -------------------------
    https://developer.help.paycom.uz/metody-subscribe-api/
    """
    def __init__(
        self,
        base_url: str,
        paycom_id: str,
        timeout=5
    ) -> "PaymeSubscribeCards":
        self.base_url: str = base_url
        self.timeout: int = timeout
        self.headers: dict = {
            "X-Auth": paycom_id,
        }
        self.__methods: dict = {
            "cards_check": "cards.check",
            "cards_create": "cards.create",
            "cards_remove": "cards.remove",
            "cards_verify": "cards.verify",
            "cards_get_verify_code": "cards.get_verify_code",
        }

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

    def cards_create(self, number: str, expire: str, save: bool = True) -> dict:
        """
        Use this method to create a new card's token.

        Parameters
        ----------
        number: str — The card number maximum length 18 char
        expire: str — The card expiration string maximum length 5 char
        save: bool \
            Type of token. Optional parameter
            The option is enabled or disabled depending on the application's business logic
            If the flag is true, the token can be used for further payments
            if the flag is false the token can only be used once
            The one-time token is deleted after payment

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/cards.create
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
        return self.__request(to_json(**data))

    def card_get_verify_code(self, token: str) -> dict:
        """
        Use this method to get the verification code.

        Parameters
        ----------
        token: str — The card's non-active token

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/cards.get_verify_code
        """
        data: dict = {
            "method": self.__methods.get('cards_get_verify_code'),
            "params": {
                "token": token,
            }
        }
        return self.__request(to_json(**data))

    def cards_verify(self, verify_code: int, token: str) -> dict:
        """
        Verification of the card using the code sent via SMS.

        Parameters
        ----------
        verify_code: int — Code for verification
        token: str — The card's non-active token

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/cards.verify
        """
        data: dict = {
            "method": self.__methods.get("cards_verify"),
            "params": {
                "token": token,
                "code": verify_code
            }
        }
        return self.__request(to_json(**data))

    def cards_check(self, token: str) -> dict:
        """
        Checking the card token active or non-active.

        Parameters
        ----------
        token: str — The card's non-active token

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/cards.check
        """
        data: dict = {
            "method": self.__methods.get("cards_check"),
            "params": {
                "token": token,
            }
        }

        return self.__request(to_json(**data))

    def cards_remove(self, token: str) -> dict:
        """
        Delete card's token on success returns success.

        Parameters
        ----------
        token: str — The card's non-active token

        Full method documentation
        -------------------------
        https://developer.help.paycom.uz/metody-subscribe-api/cards.remove
        """
        data: dict = {
            "method": self.__methods.get("cards_remove"),
            "params": {
                "token": token,
            }
        }
        return self.__request(to_json(**data))
