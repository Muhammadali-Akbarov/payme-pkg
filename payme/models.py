from django.db import models
from django.conf import settings
from django.utils import timezone

from django.utils.module_loading import import_string

from payme.const import PaymeReasonCodesEnum
from payme.const import PaymeTransactionStateEnum as Status


AccountModel = import_string(settings.PAYME_ACCOUNT_MODEL)


class PaymeTransactions(models.Model):
    """
    Model to store payment transactions.
    """
    account_related_name = "payme_transactions"
    state_choices = Status.choices()
    cancel_reason_choices = PaymeReasonCodesEnum.choices()
    state_default = Status.CREATED.value

    transaction_id = models.CharField(max_length=50)
    account = models.ForeignKey(
        AccountModel,
        related_name=account_related_name,
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.IntegerField(choices=state_choices, default=state_default)
    cancel_reason = models.IntegerField(
        choices=cancel_reason_choices, null=True, blank=True
    )
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
        return f"Payme Transaction #{self.transaction_id} Account: {self.account} - {self.state}" # noqa

    @classmethod
    def get_or_create(
        cls, transaction_id,
        amount, state, account
    ) -> tuple["PaymeTransactions", bool]:
        """
        Class method to get or create a PaymentTransaction instance.

        :param transaction_id: The unique ID of the transaction.
        :param amount: The amount for the transaction.
        :param state: The current state of the transaction.
        :param account: The related account instance for the transaction.
        :return: (instance, created) tuple where 'instance' is the
            PaymentTransaction instance and 'created' is a boolean indicating
                if it was created or not.
        """
        transaction, created = cls.objects.get_or_create(
            account=account,
            defaults={
                'amount': amount,
                'state': state,
                'transaction_id': transaction_id
            }
        )
        return transaction, created

    @classmethod
    def get_by_transaction_id(cls, transaction_id):
        """
        Class method to get a PaymentTransaction instance by its transaction ID. # noqa

        :param transaction_id: The unique ID of the transaction.
        :return: The PaymentTransaction instance or None if not found.
        """
        return cls.objects.get(transaction_id=transaction_id)

    def is_performed(self) -> bool:
        """
        Check if the transaction is completed.

        :return: True if the transaction is completed, False otherwise.
        """
        return self.state == Status.WITHDRAWAL_IN_PROGRESS_2.value

    def is_cancelled(self) -> bool:
        """
        Check if the transaction is cancelled.

        :return: True if the transaction is cancelled, False otherwise.
        """
        return self.state in [
            Status.CANCELED.value,
            Status.CANCELLED_WITHDRAWAL_IN_PROGRESS_2.value,
            Status.CANCELLED_AFTER_WITHDRAWAL_IN_PROGRESS_1.value
        ]

    def is_created(self) -> bool:
        """
        Check if the transaction is created.

        :return: True if the transaction is created, False otherwise.
        """
        return self.state == Status.CREATED.value

    def is_created_in_payme(self) -> bool:
        """
        Check if the transaction was created in Payme.

        :return: True if the transaction was created in Payme, False otherwise.
        """
        return self.state == Status.WITHDRAWAL_IN_PROGRESS_1.value

    def mark_as_cancelled(
        self, cancel_reason: int, state: int
    ) -> "PaymeTransactions":
        """
        Mark the transaction as cancelled.

        :param cancel_reason: The reason for cancelling the transaction.
        :return:True if the transaction was successfully marked as cancelled, False otherwise. # noqa
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

        :return: True if the transaction was successfully marked as performed, False otherwise. # noqa
        """
        if self.state != Status.WITHDRAWAL_IN_PROGRESS_1.value:
            return False

        self.state = Status.WITHDRAWAL_IN_PROGRESS_2.value
        self.performed_at = timezone.now()
        self.save()
        return True
