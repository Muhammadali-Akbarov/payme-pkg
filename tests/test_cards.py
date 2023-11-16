from tests.base import BaseTestCase


class SubscribeCardsTest(BaseTestCase):
    # pylint: disable=missing-class-docstring
    def test_cards_create(self) -> None:
        self._test_cards_create()

    def test_cards_verify(self) -> None:
        self._test_cards_verify()

    def test_cards_check(self) -> None:
        response = self.subscribe_client.cards_check(self.get_data()["token"])
        card = response["result"]["card"]

        self.assertEqual(card["number"], "860006******6311")
        self.assertEqual(card["expire"], "03/99")
        self.assertTrue(card["recurrent"])
        self.assertTrue(card["verify"])
        self.assertEqual(card["type"], "22618")

    def test_cards_remove(self) -> None:
        response = self.subscribe_client.cards_remove(self.get_data()["token"])

        self.assertTrue(response["result"]["success"])
