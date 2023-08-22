from django.contrib import admin

from payme.models import CUSTOM_ORDER
from payme.models import Order as DefaultOrderModel

from payme.models import MerchatTransactionsModel

if not CUSTOM_ORDER:
    admin.site.register(DefaultOrderModel)

admin.site.register(MerchatTransactionsModel)
