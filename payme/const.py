"""
Payme enumerations
"""
from enum import StrEnum, IntEnum


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


class PaymeTransactionStateEnum(IntEnum):
    """
    The enumeration of possible payment states during the transaction process.

    States:
    - CREATED (0): Check created. Awaiting payment confirmation.
    - WITHDRAWAL_IN_PROGRESS_1 (1):
        Creating a transaction in the provider's billing system.
    - WITHDRAWAL_IN_PROGRESS_2 (2): Deducting money from the card.
    - WITHDRAWAL_CLOSING (3):
        Closing the transaction in the provider's billing system.
    - PERFORMED (4): Check paid successfully.
    - WAITING_TO_BE_CHECKED (20): Check is paused for manual intervention.
    - WAITING_TO_BE_CANCELLED_1 (21): Check is queued for cancellation.
    - WAITING_TO_BE_CANCELLED_2 (30):
        Check is queued for closing the transaction in the provider's billing system. # Noqa
    - CANCELED (50): Check canceled.
    - CANCELLED_WITHDRAWAL_IN_PROGRESS_2 (-2):
        Canceled after the second withdrawal stage.
    - CANCELLED_AFTER_WITHDRAWAL_IN_PROGRESS_1 (-1): Canceled after the first withdrawal stage.
    """
    # PENDING states
    CREATED = 0
    WITHDRAWAL_IN_PROGRESS_1 = 1
    WITHDRAWAL_IN_PROGRESS_2 = 2
    WITHDRAWAL_CLOSING = 3

    # SUCCESSFUL state
    SUCCESS = 4

    # States indicating the transaction will be cancelled or paused
    WAITING_TO_BE_CHECKED = 20
    WAITING_TO_BE_CANCELLED_1 = 21
    WAITING_TO_BE_CANCELLED_2 = 30

    # CANCELED state
    CANCELED = 50
    CANCELLED_WITHDRAWAL_IN_PROGRESS_2 = -2
    CANCELLED_AFTER_WITHDRAWAL_IN_PROGRESS_1 = -1

    def __str__(self):
        return f"Payment state {self.name} (Code: {self.value})"

    @classmethod
    def choices(cls):
        """
        Provides choices for Django models' `choices` field argument.
        """
        return [(state.value, state.name) for state in cls]


class PaymeReasonCodesEnum(IntEnum):
    """
    Enum class for Payme error codes,
    representing different error states that can occur during a transaction.

    Error Codes:
    - RECIPIENT_NOT_FOUND (1):
        One or more recipients not found or inactive in Payme Business.
    - DEBIT_OPERATION_FAILED (2):
        Error during debit operation in the processing center.
    - TRANSACTION_FAILED (3): Error executing the transaction.
    - TRANSACTION_TIMEOUT (4): Transaction canceled due to timeout.
    - REFUND (5): Refund issued.
    - UNKNOWN_ERROR (10): Unknown error.
    """
    RECIPIENT_NOT_FOUND = 1
    DEBIT_OPERATION_FAILED = 2
    TRANSACTION_FAILED = 3
    TRANSACTION_TIMEOUT = 4
    REFUND = 5
    UNKNOWN_ERROR = 10

    @classmethod
    def choices(cls):
        """
        Provides choices for Django models' `choices` field argument.
        """
        return [(state.value, state.name) for state in cls]


class Networks(StrEnum):
    """
    Payme networks
    """
    PROD_NET = "https://checkout.paycom.uz/api"
    TEST_NET = "https://checkout.test.paycom.uz/api"
