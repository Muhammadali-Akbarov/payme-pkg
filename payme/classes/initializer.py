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

    def __init__(self, payme_id: str = None):
        self.payme_id = payme_id

    def generate_pay_link(
        self,
        id: int,
        amount: int,
        return_url: str
    ) -> str:
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
        params = (
            f'm={self.payme_id};ac.{settings.PAYME_ACCOUNT_FIELD}={id};a={amount};c={return_url}'
        )
        params = base64.b64encode(params.encode("utf-8")).decode("utf-8")
        return f"https://checkout.paycom.uz/{params}"
