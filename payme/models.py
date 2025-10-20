"""
This module contains models and functionality for tracking changes in payment transactions.
It logs any significant modifications to payment transactions such as amount, state, or payment method,
allowing for a detailed historical record of each transaction's state over time.
"""
from django.db import models
from django.utils import timezone


class PaymeTransactions(models.Model):
    """
    Model to store payment transactions.
    """
    CREATED = 0
    INITIATING = 1
    SUCCESSFULLY = 2
    CANCELED = -2
    CANCELED_DURING_INIT = -1

    STATE = [
        (CREATED, "Created"),
        (INITIATING, "Initiating"),
        (SUCCESSFULLY, "Successfully"),
        (CANCELED, "Canceled after successful performed"),
        (CANCELED_DURING_INIT, "Canceled during initiation"),
    ]

    transaction_id = models.CharField(max_length=50)
    account_id = models.CharField(max_length=256, null=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    state = models.IntegerField(choices=STATE, default=CREATED)
    fiscal_data = models.JSONField(default=dict)
    cancel_reason = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    performed_at = models.DateTimeField(null=True, blank=True, db_index=True)
    cancelled_at = models.DateTimeField(null=True, blank=True, db_index=True)

    class Meta:
        """
        Model Meta options.
        """
        verbose_name = "Payme Transaction"
        verbose_name_plural = "Payme Transactions"
        ordering = ["-created_at"]
        db_table = "payme_transactions"

    def __str__(self):
        """
        String representation of the PaymentTransaction model.
        """
        return f"Payme Transaction #{self.transaction_id} Account: {self.account_id} - {self.state}"

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        """
        Class method to get a PaymentTransaction instance by its transaction ID.

        :param transaction_id: The unique ID of the transaction.
        :return: The PaymentTransaction instance or None if not found.
        """
        return cls.objects.get(transaction_id=transaction_id)

    def is_performed(self) -> bool:
        """
        Check if the transaction is completed.

        :return: True if the transaction is completed, False otherwise.
        """
        return self.state == self.SUCCESSFULLY

    def is_cancelled(self) -> bool:
        """
        Check if the transaction is cancelled.

        :return: True if the transaction is cancelled, False otherwise.
        """
        return self.state in [
            self.CANCELED,
            self.CANCELED_DURING_INIT
        ]

    def is_created(self) -> bool:
        """
        Check if the transaction is created.

        :return: True if the transaction is created, False otherwise.
        """
        return self.state == self.CREATED

    def is_created_in_payme(self) -> bool:
        """
        Check if the transaction was created in Payme.

        :return: True if the transaction was created in Payme, False otherwise.
        """
        return self.state == self.INITIATING

    def mark_as_cancelled(self, cancel_reason: int, state: int) -> "PaymeTransactions":
        """
        Mark the transaction as cancelled.

        :param cancel_reason: The reason for cancelling the transaction.
        :return: True if the transaction was successfully marked as cancelled, False otherwise.
        """
        if self.state == state:
            return self

        self.state = state
        self.cancel_reason = cancel_reason
        self.cancelled_at = timezone.now()
        self.save()
        return self

    def mark_as_performed(self) -> bool:
        """
        Mark the transaction as performed.

        :return: True if the transaction was successfully marked as performed, False otherwise.
        """
        if self.state != self.INITIATING:
            return False

        self.state = self.SUCCESSFULLY
        self.performed_at = timezone.now()
        self.save()
        return True
