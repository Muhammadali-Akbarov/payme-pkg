"""
Payme enumerations
"""
from enum import StrEnum


class Methods(StrEnum):
    """
    The enumeration of create transaction methods.

    Available Methods:
    - GET_STATEMENT: Fetches transaction statement.
    - CHECK_TRANSACTION: Checks a transaction.
    - CREATE_TRANSACTION: Creates a new transaction.
    - CANCEL_TRANSACTION: Cancels an existing transaction.
    - PERFORM_TRANSACTION: Performs a transaction.
    - CHECK_PERFORM_TRANSACTION: Checks if the transaction can be performed.
    """
    GET_STATEMENT = "GetStatement"
    CHECK_TRANSACTION = "CheckTransaction"
    CREATE_TRANSACTION = "CreateTransaction"
    CANCEL_TRANSACTION = "CancelTransaction"
    PERFORM_TRANSACTION = "PerformTransaction"
    CHECK_PERFORM_TRANSACTION = "CheckPerformTransaction"

    def __str__(self):
        return str(self.value)


class Networks(StrEnum):
    """
    Payme networks
    """
    PROD_NET = "https://checkout.paycom.uz/api"
    TEST_NET = "https://checkout.test.paycom.uz/api"
