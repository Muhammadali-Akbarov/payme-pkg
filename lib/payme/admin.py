from django.contrib import admin

from payme.models import Order as DefaultOrderModel
from payme.models import MerchatTransactionsModel

admin.site.register(DefaultOrderModel)
admin.site.register(MerchatTransactionsModel)
