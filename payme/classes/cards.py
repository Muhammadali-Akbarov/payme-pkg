from typing import Optional

from payme.classes.http import HttpClient
from payme.types.response import cards as response


ALLOWED_METHODS = {
    "cards.create": response.CardsCreateResponse,
    "cards.get_verify_code": response.GetVerifyResponse,
    "cards.verify": response.VerifyResponse,
    "cards.remove": response.RemoveResponse,
    "cards.check": response.CheckResponse
}


class Cards:
    """
    The Cards class provides a simple interface to interact with Paycom card
    services. It allows you to create new cards and retrieve verification
    codes for existing cards.
    """
    def __init__(self, url: str, payme_id: str) -> None:
        """
        Initialize the Cards client.

        :param payme_id: The Paycom ID used for authentication.
        :param url: The base URL for the Paycom card service API.
        """
        headers = {
            "X-Auth": payme_id,
            "Content-Type": "application/json"
        }
        self.http = HttpClient(url, headers)

    def create(self, number: str, expire: str, save: bool = False,
               timeout: int = 10) -> response.CardsCreateResponse:
        """
        Create a new card.

        :param number: The card number.
        :param expire: The expiration date of the card in MMYY format.
        :param save: A boolean indicating whether to save the card for future
            use (default is False).
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A CardsCreateResponse object containing the response data.
        """
        method = "cards.create"
        params = {"card": {"number": number, "expire": expire}, "save": save}
        return self._post_request(method, params, timeout)

    def get_verify_code(self, token: str, timeout: int = 10) -> \
            response.GetVerifyResponse:
        """
        Retrieve a verification code for a specified token.

        :param token: The token associated with the card.
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A GetVerifyResponse object containing the response data.
        """
        method = "cards.get_verify_code"
        params = {"token": token}
        return self._post_request(method, params, timeout)

    def verify(self, token: str, code: str, timeout: int = 10) -> \
            response.VerifyResponse:
        """
        Verify a verification code for a specified token.

        :param token: The token associated with the card.
        :param code: The verification code to be verified.
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A VerifyResponse object containing the response data.
        """
        method = "cards.verify"
        params = {"token": token, "code": code}
        return self._post_request(method, params, timeout)

    def remove(self, token: str, timeout: int = 10) -> response.RemoveResponse:
        """
        Remove a card from the Paycom system.

        :param token: The token associated with the card.
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A RemoveResponse object containing the response data.
        """
        method = "cards.remove"
        params = {"token": token}
        return self._post_request(method, params, timeout)

    def check(self, token: str, timeout: int = 10) -> response.CheckResponse:
        """
        Check the status of a card.

        :param token: The token associated with the card.
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A CheckResponse object containing the response data.
        """
        method = "cards.check"
        params = {"token": token}
        return self._post_request(method, params, timeout)

    def _post_request(self, method: str, params: dict,
                      timeout: int = 10) -> response.Common:
        """
        Helper method to post requests to the HTTP client.

        :param method: The API method to be called.
        :param params: The parameters to be sent with the request.
        :param timeout: The request timeout duration in seconds (default is
            10 seconds).
        :return: A response object corresponding to the method called.
        """
        json = {"method": method, "params": params}
        dict_result = self.http.post(json, timeout)
        response_class = ALLOWED_METHODS[method]
        return response_class.from_dict(dict_result)

    def test(self):
        """
        Run a comprehensive test suite for card functionalities including
        creation, verification, status check, and removal.
        """
        # Expected values for verification
        number = "8600495473316478"
        expire = "0399"

        expected_number = "860049******6478"
        expected_expire = "03/99"
        verify_code = "666666"

        # Step 1: Create Card
        create_response = self.create(number=number, expire=expire)
        token = create_response.result.card.token

        # Validate card creation response
        self._assert_and_print(
            create_response.result.card.number == expected_number,
            "Card number matched.",
            test_case="Card Creation - Number Validation"
        )
        self._assert_and_print(
            create_response.result.card.expire == expected_expire,
            "Expiration date matched.",
            test_case="Card Creation - Expiration Date Validation"
        )

        # Step 2: Get Verification Code
        get_verify_response = self.get_verify_code(token=token)
        self._assert_and_print(
            get_verify_response.result.sent is True,
            "Verification code requested successfully.",
            test_case="Verification Code Request"
        )

        # Step 3: Verify Code
        verify_response = self.verify(token=token, code=verify_code)
        self._assert_and_print(
            verify_response.result.card.verify is True,
            "Verification code validated successfully.",
            test_case="Code Verification"
        )

        # Step 4: Check Card Status
        check_response = self.check(token=token)
        self._assert_and_print(
            check_response.result.card.verify is True,
            "Card status verified successfully.",
            test_case="Card Status Check"
        )

        # Step 5: Remove Card
        remove_response = self.remove(token=token)
        self._assert_and_print(
            remove_response.result.success is True,
            "Card removed successfully.",
            test_case="Card Removal"
        )

    def _assert_and_print(self, condition: bool, success_message: str,
                          test_case: Optional[str] = None):
        """
        Assertion helper that prints success or failure messages based on
        test outcomes.

        :param condition: The test condition to check.
        :param success_message: Message to print upon successful test.
        :param test_case: A description of the test case (optional).
        """
        try:
            assert condition, "Assertion failed!"
            print(f"Success: {success_message}")
        except AssertionError as exc:
            error_message = (
                f"Test Case Failed: {test_case or 'Unknown Test Case'}\n"
                f"Error Details: {str(exc)}"
            )
            print(error_message)
            raise AssertionError(error_message) from exc
