import base64

from payme.util import input_type_checker


class Initializer:
    """
    Initialize the Payme class with necessary details.

    Attributes
    ----------
    payme_id: str
        The Payme ID associated with your account
    """

    @input_type_checker
    def __init__(self, payme_id: str = None):
        self.payme_id = payme_id

    # pylint: disable=W0622
    @input_type_checker
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
            f'm={self.payme_id};ac.id={id};a={amount};c={return_url}'
        )
        params = base64.b64encode(params.encode("utf-8")).decode("utf-8")
        return f"https://checkout.paycom.uz/{params}"

    def test(self):
        """
        Test method for the Initializer class.

        This method generates a payment link for a sample order and checks
        if the result is a valid string. If successful, it prints a
        confirmation message.
        """
        result = self.generate_pay_link(
            id=12345,
            amount=7000,
            return_url="https://example.com"
        )

        assert isinstance(result, str), "Failed to generate payment link"
        print("Success: Payment link generated successfully.")
