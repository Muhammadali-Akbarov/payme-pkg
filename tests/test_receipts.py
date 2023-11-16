from tests.base import BaseTestCase


class ReceiptsTest(BaseTestCase):
    # pylint: disable=missing-class-docstring
    def assert_receipts_data(self, response) -> None:
        card = response["result"]["receipt"]["card"]

        self.assertEqual(card["expire"], "9903")
        self.assertEqual(card["number"], "860006******6311")
        self.assertEqual(response["result"]["receipt"]["amount"], 10000)
        self.assertEqual(response["result"]["receipt"]["payer"]["phone"], "998901304527")

    def test_cards_create(self) -> None:
        self._test_cards_create()
        self._test_cards_verify()

    def test_receipts_create(self) -> None:
        response = self.receipts_client.receipts_create(
            amount=10000,
            order_id="1",
        )
        self.assertEqual(response["result"]["receipt"]["amount"], 10000)

        self.update_data(invoice_id=response["result"]["receipt"]["_id"])

    def test_receipts_pay(self) -> None:
        response = self.receipts_client.receipts_pay(
            invoice_id=self.get_data()["invoice_id"],
            token=self.get_data()["token"],
            phone="998901304527",
        )
        self.assert_receipts_data(response)

    def test_receipts_send(self) -> None:
        response = self.receipts_client.receipts_send(
            invoice_id=self.get_data()["invoice_id"],
            phone="998901304527",
        )
        self.assertTrue(response["result"]["success"])

    def test_receipts_check(self) -> None:
        response = self.receipts_client.receipts_check(
            invoice_id=self.get_data()["invoice_id"],
        )
        self.assertEqual(response["result"]["state"], 4)

    def test_receipts_get(self) -> None:
        response = self.receipts_client.receipts_get(
            invoice_id=self.get_data()["invoice_id"],
        )
        self.assert_receipts_data(response)

    def test_receipts_get_all(self) -> None:
        response = self.receipts_client.receipts_get_all(
            count=2,
            _from=1636398000000,
            _to=1636398000000,
            offset=0,
        )
        self.assertEqual(len(response["result"]), 2)

    def test_receipts_cancel(self) -> None:
        response = self.receipts_client.receipts_cancel(
            invoice_id=self.get_data()["invoice_id"],
        )
        self.assertEqual(response["result"]["receipt"]["meta"]["source_cancel"], "subscribe")
