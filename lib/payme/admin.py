from django.contrib import admin

from payme.models import Order
from payme.models import MerchatTransactionsModel

admin.site.register(Order)
admin.site.register(MerchatTransactionsModel)
