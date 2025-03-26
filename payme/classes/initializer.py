import base64

from django.conf import settings


class Initializer:
    """
    Initialize the Payme class with necessary details.

    Attributes
    ----------
    payme_id: str
        The Payme ID associated with your account
    """

    def __init__(
        self, payme_id: str = None, fallback_id: str = None, is_test_mode: bool = False
    ) -> None:
        self.payme_id = payme_id
        self.fallback_id = fallback_id
        self.is_test_mode = is_test_mode

    def generate_pay_link(self, id: int, amount: int, return_url: str) -> str:
        """
        Generate a payment link for a specific order.

        This method encodes the payment parameters into a base64 string and
        constructs a URL for the Payme checkout.

        Parameters
        ----------
        id : int
            Unique identifier for the account.
        amount : int
            The amount associated with the order in currency units.
        return_url : str
            The URL to which the user will be redirected after the payment is
            processed.

        Returns
        -------
        str
            A payment link formatted as a URL, ready to be used in the payment
            process.

        References
        ----------
        For full method documentation, visit:
        https://developer.help.paycom.uz/initsializatsiya-platezhey/
        """
        amount = amount * 100  # Convert amount to the smallest currency unit
        params = f"m={self.payme_id};ac.{settings.PAYME_ACCOUNT_FIELD}={id};a={amount};c={return_url}"
        params = base64.b64encode(params.encode("utf-8")).decode("utf-8")

        if self.is_test_mode is True:
            return f"https://test.paycom.uz/{params}"

        return f"https://checkout.paycom.uz/{params}"

    def generate_fallback_link(self, form_fields: dict = None):
        """
        Generate a fallback URL for the Payme checkout.

        Parameters
        ----------
        fields : dict, optional
            Additional query parameters to be appended to the fallback URL.

        Returns
        -------
        str
            A fallback URL formatted as a URL, ready to be used in the payment
            process.
        """
        result = f"https://payme.uz/fallback/merchant/?id={self.fallback_id}"

        if form_fields is not None:
            for key, value in form_fields.items():
                result += f"&{key}={value}"

        return result
