from django.db import models


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


class ShippingDetail(models.Model):
    """
    ShippingDetail class \
        That's used for managing shipping
    """
    title = models.CharField(max_length=255)
    price = models.FloatField(default=0)

    def __str__(self) -> str:
        return f"[{self.pk}] {self.title} {self.price}"


class Item(models.Model):
    """
    Item class \
        That's used for managing order items
    """
    discount = models.FloatField(null=True, blank=True)
    title = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    count = models.IntegerField(default=1)
    code = models.CharField(max_length=17)
    units = models.IntegerField(null=True, blank=True)
    package_code = models.CharField(max_length=255)
    vat_percent = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f"[{self.id}] {self.title} #{self.code}"


class OrderDetail(models.Model):
    """
    OrderDetail class \
        That's used for managing order details
    """
    receipt_type = models.IntegerField(default=0)
    shipping = models.ForeignKey(
        to=ShippingDetail,
        null=True, blank=True,
        on_delete=models.CASCADE
    )
    items = models.ManyToManyField(Item)

    def get_items_display(self):
        # pylint: disable=missing-function-docstring
        return ', '.join([items.title for items in self.items.all()])

    def __str__(self) -> str:
        return f"[{self.pk}] {self.get_items_display()}"


class DisallowOverrideMetaclass(models.base.ModelBase):
    # pylint: disable=missing-class-docstring
    def __new__(mcs, name, bases, attrs: dict, **kwargs):
        disallowed_fields = ['amount', 'detail']

        if name != 'BaseOrder':
            for field_name in disallowed_fields:
                if not attrs.get(field_name):
                    continue

                raise TypeError(
                    f"Field '{field_name}' in '{name}' cannot be overridden."
                )

        return super().__new__(mcs, name, bases, attrs, **kwargs)


class BaseOrder(models.Model, metaclass=DisallowOverrideMetaclass):
    """
    Order class \
        That's used for managing order process
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    amount = models.FloatField(null=True, blank=True)
    detail = models.ForeignKey(
        OrderDetail,
        null=True, blank=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"ORDER ID: {self.id} - AMOUNT: {self.amount}"

    class Meta:
        # pylint: disable=missing-class-docstring
        abstract = True
