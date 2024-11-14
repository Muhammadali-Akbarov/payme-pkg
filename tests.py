import os

import unittest
from payme import Payme


class TestPaymeAPI(unittest.TestCase):
    """
    Test Payme API methods
    """
    @classmethod
    def setUpClass(cls):
        """
        Initialize the Payme client in test mode
        """
        cls.payme = Payme(
            payme_id=os.getenv("PAYME_ID"),
            payme_key=os.getenv("PAYME_KEY"),
            is_test_mode=True
        )

    def test_cards_all_methods(self):
        """
        Verify that the cards test method works without errors
        """
        return self.payme.cards.test()

    def test_receipts_all_methods(self):
        """
        Verify that the receipts test method works without errors
        """
        return self.payme.receipts.test()


if __name__ == '__main__':
    unittest.main()
