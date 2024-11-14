
from typing import Union

from payme.const import Networks
from payme.classes.cards import Cards
from payme.classes.receipts import Receipts
from payme.classes.initializer import Initializer


class Payme:
    """
    The payme class provides a simple interface
    """
    def __init__(
        self,
        payme_id: str,
        payme_key: Union[str, None] = None,
        is_test_mode: bool = False
    ):

        # initialize payme network
        url = Networks.PROD_NET

        if is_test_mode is True:
            url = Networks.TEST_NET.value

        self.cards = Cards(url=url, payme_id=payme_id)
        self.initializer = Initializer(payme_id=payme_id)
        self.receipts = Receipts(url=url, payme_id=payme_id, payme_key=payme_key)  # noqa
