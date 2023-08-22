from django.db import models
from django.conf import settings
from django.utils.module_loading import import_string
from django.core.exceptions import FieldError

from payme.utils.logging import logger


class MerchatTransactionsModel(models.Model):
    """
    MerchatTransactionsModel class \
        That's used for managing transactions in database.
    """
    _id = models.CharField(max_length=255, null=True, blank=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=False)
    order_id = models.BigIntegerField(null=True, blank=True)
    amount = models.FloatField(null=True, blank=True)
    time = models.BigIntegerField(null=True, blank=True)
    perform_time = models.BigIntegerField(null=True, default=0)
    cancel_time = models.BigIntegerField(null=True, default=0)
    state = models.IntegerField(null=True, default=1)
    reason = models.CharField(max_length=255, null=True, blank=True)
    created_at_ms = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self._id)


try:
    CUSTOM_ORDER = import_string(settings.ORDER_MODEL)

    if not isinstance(CUSTOM_ORDER, models.base.ModelBase):
        raise TypeError("The input must be an instance of models.Model class")

    # pylint: disable=protected-access
    if 'amount' not in [f.name for f in CUSTOM_ORDER._meta.fields]:
        raise FieldError("Missing 'amount' field in your custom order model")

    Order = CUSTOM_ORDER
except (ImportError, AttributeError):
    logger.warning("You have no payme custom order model")

    CUSTOM_ORDER = None

    class Order(models.Model):
        """
        Order class \
            That's used for managing order process
        """
        amount = models.IntegerField(null=True, blank=True)
        created_at = models.DateTimeField(auto_now_add=True)
        updated_at = models.DateTimeField(auto_now=True)

        def __str__(self):
            return f"ORDER ID: {self.id} - AMOUNT: {self.amount}"

        class Meta:
            # pylint: disable=missing-class-docstring
            managed = False
