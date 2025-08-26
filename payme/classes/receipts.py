import typing as t

from urllib.parse import parse_qs

from payme.classes.cards import Cards
from payme.classes.http import HttpClient
from payme.types.response import receipts as response


ALLOWED_METHODS = {
    "receipts.create": response.CreateResponse,
    "receipts.pay": response.PayResponse,
    "receipts.send": response.SendResponse,
    "receipts.cancel": response.CancelResponse,
    "receipts.check": response.CheckResponse,
    "receipts.get": response.GetResponse,
    "receipts.get_all": response.GetAllResponse,
    "receipts.set_fiscal_data": response.SetFiscalDataResponse,
}


class Receipts:
    """
    The Receipts class provides methods to interact with the Payme Receipts.
    """

    def __init__(self, payme_id: str, payme_key: str, url: str) -> None:
        """
        Initialize the Receipts client.

        :param payme_id: The Payme ID associated with your account.
        :param payme_key: The Payme API key associated with your account.
        :param url: The base URL for the Payme Receipts API.
        """
        self.__cards = Cards(url, payme_id)

        headers = {
            "X-Auth": f"{payme_id}:{payme_key}",
            "Content-Type": "application/json",
        }
        self.http = HttpClient(url, headers)

    def create(
        self,
        account: dict,
        amount: t.Union[float, int],
        description: t.Optional[str] = None,
        detail: t.Optional[t.Dict] = None,
        timeout: int = 10,
    ) -> response.CreateResponse:
        """
        Create a new receipt.

        :param account: The account details for the receipt.
        :param amount: The amount of the receipt.
        :param description: t.Optional description for the receipt.
        :param detail: t.Optional additional details for the receipt.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.create"
        params = {
            "amount": amount,
            "account": account,
            "description": description,
            "detail": detail,
        }
        return self._post_request(method, params, timeout)

    def pay(
        self, receipts_id: str, token: str, timeout: int = 10
    ) -> response.PayResponse:
        """
        Pay the receipt using a cheque.

        :param receipts_id: The ID of the cheque used for payment.
        :param token: The token associated with the cheque.
        :param timeout:
            The request timeout duration in seconds (default is 10).
        """
        method = "receipts.pay"
        params = {"id": receipts_id, "token": token}
        return self._post_request(method, params, timeout)

    def send(
        self, receipts_id: str, phone: str, timeout: int = 10
    ) -> response.SendResponse:
        """
        Send the receipt to a mobile phone.

        :param receipts_id: The ID of the cheque used for payment.
        :param phone: The phone number to send the receipt to.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.send"
        params = {"id": receipts_id, "phone": phone}
        return self._post_request(method, params, timeout)

    def cancel(self, receipts_id: str, timeout: int = 10) -> response.CancelResponse:
        """
        Cancel the receipt.

        :param receipts_id: The ID of the cheque used for payment.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.cancel"
        params = {"id": receipts_id}
        return self._post_request(method, params, timeout)

    def check(self, receipts_id: str, timeout: int = 10) -> response.CheckResponse:
        """
        Check the status of a cheque.

        :param receipts_id: The ID of the cheque used for payment.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.check"
        params = {"id": receipts_id}
        return self._post_request(method, params, timeout)

    def get(self, receipts_id: str, timeout: int = 10) -> response.GetResponse:
        """
        Get the details of a specific cheque.

        :param receipts_id: The ID of the cheque used for payment.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.get"
        params = {"id": receipts_id}
        return self._post_request(method, params, timeout)

    def get_all(
        self, count: int, from_: int, to: int, offset: int, timeout: int = 10
    ) -> response.GetAllResponse:
        """
         Get all cheques for a specific account.

         :param count: The number of cheques to retrieve.
         :param from_: The start index of the cheques to retrieve.
         :param to: The end index of the cheques to retrieve.
         :param offset: The offset for pagination.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.get_all"
        params = {"count": count, "from": from_, "to": to, "offset": offset}
        return self._post_request(method, params, timeout)

    def set_fiscal_data(
        self, receipt_id: str, qr_code_url: str, timeout: int = 10
    ) -> response.SetFiscalDataResponse:
        """
        Get all cheques for a specific account.

        :param receipt_id: The ID of the check used for payment.
        :param qr_code_url: URL of the fiscal check from the ofd.uz.
        :param timeout: The request timeout duration in seconds (default 10).
        """
        method = "receipts.set_fiscal_data"

        check_params = parse_qs(qr_code_url.split("?")[1])
        terminal_id = check_params["t"][0]
        fiscal_sign = check_params["s"][0]
        fiscal_receipt_id = check_params["r"][0]
        fiscal_date = check_params["c"][0]

        params = {
            "id": receipt_id,  # required
            "fiscal_data": {
                "terminal_id": terminal_id,
                "receipt_id": int(fiscal_receipt_id),  # required
                "date": fiscal_date,
                "fiscal_sign": fiscal_sign,
                "qr_code_url": qr_code_url,  # required
            }
        }
        return self._post_request(method, params, timeout)

    def _post_request(
        self, method: str, params: dict, timeout: int = 10
    ) -> response.Common:
        """
        Helper method to post requests to the HTTP client.

        :param method: The API method to be called.
        :param params: The parameters to be sent with the request.
        :param timeout: The request timeout duration in seconds (default 10).
        :return: A response object corresponding to the method called.
        """
        json = {"method": method, "params": params}
        dict_result = self.http.post(json, timeout)
        response_class = ALLOWED_METHODS[method]
        return response_class.from_dict(dict_result)

    def test(self):
        """
        Run a comprehensive suite of tests for the Receipts class,
        covering creation, payment, sending, cancellation, status checks,
        retrieval of a single receipt, and retrieval of multiple receipts.
        """

        # Helper to assert conditions with messaging
        def assert_condition(condition, message, test_case):
            self._assert_and_print(condition, message, test_case=test_case)

        # Helper to create a receipt for reuse
        def create_sample_receipt():
            return self.create(
                account={"id": 12345},
                amount=1000,
                description="Test receipt",
                detail={"key": "value"},
            )

        # Test 1: Initialization check
        assert_condition(
            isinstance(self, Receipts),
            "Initialized Receipts class successfully.",
            test_case="Initialization Test",
        )

        # Test 2: Create and Pay Receipt
        create_response = create_sample_receipt()
        assert_condition(
            isinstance(create_response, response.CreateResponse),
            "Created a new receipt successfully.",
            test_case="Receipt Creation Test",
        )

        # pylint: disable=W0212
        assert_condition(
            isinstance(create_response.result.receipt._id, str),
            "Created a valid receipt ID.",
            test_case="Receipt ID Test",
        )

        # Prepare card and verification
        cards_create_response = self.__cards.create(
            number="8600495473316478", expire="0399", save=True
        )
        token = cards_create_response.result.card.token
        self.__cards.get_verify_code(token=token)
        self.__cards.verify(token=token, code="666666")

        # Pay receipt and verify payment state
        receipt_id = create_response.result.receipt._id
        pay_response = self.pay(receipts_id=receipt_id, token=token)
        assert_condition(
            pay_response.result.receipt.state == 4,
            "Paid the receipt successfully.",
            test_case="Payment Test",
        )

        # Test 3: Create and Send Receipt
        create_response = create_sample_receipt()
        receipt_id = create_response.result.receipt._id
        send_response = self.send(receipts_id=receipt_id, phone="998901304527")
        assert_condition(
            send_response.result.success is True,
            "Sent the receipt successfully.",
            test_case="Send Test",
        )

        # Test 4: Create and Cancel Receipt
        create_response = create_sample_receipt()
        receipt_id = create_response.result.receipt._id
        cancel_response = self.cancel(receipts_id=receipt_id)
        assert_condition(
            cancel_response.result.receipt.state == 50,
            "Cancelled the receipt successfully.",
            test_case="Cancel Test",
        )

        # Test 5: Check Receipt Status
        check_response = self.check(receipts_id=receipt_id)
        assert_condition(
            check_response.result.state == 50,
            "Checked the receipt status successfully.",
            test_case="Check Test",
        )

        # Test 6: Get Receipt Details
        get_response = self.get(receipts_id=receipt_id)
        assert_condition(
            get_response.result.receipt._id == receipt_id,
            "Retrieved the receipt details successfully.",
            test_case="Get Test",
        )

        # Test 7: Retrieve All Receipts
        get_all_response = self.get_all(
            count=1, from_=1730322122000, to=1730398982000, offset=0
        )
        assert_condition(
            isinstance(get_all_response.result, list),
            "Retrieved all receipts successfully.",
            test_case="Get All Test",
        )

    # pylint: disable=W0212
    def _assert_and_print(
        self, condition: bool, success_message: str, test_case: t.Optional[str] = None
    ):
        self.__cards._assert_and_print(condition, success_message, test_case)
