from django.contrib import admin

from payme.models import (
    Item, MerchatTransactionsModel,
    OrderDetail, ShippingDetail
)
# pylint: disable=fixme
# TODO: order Payme models in admin panel
# 1. OrderDetail
# 2. Item
# 3. ShippingDetail
# 4. MerchatTransactionsModel

admin.site.register(
    [
        OrderDetail, Item,
        ShippingDetail,
        MerchatTransactionsModel,
    ]
)
