from django.conf import settings
from django.contrib import admin

from payme.models import PaymeTransactions


class PaymeTransactionsUI(admin.ModelAdmin):
    """
    Custom admin interface for PaymeTransactions model.
    """
    list_display = ('pk', 'state', 'cancel_reason', 'created_at')
    list_filter = ('state', 'cancel_reason', 'created_at')
    search_fields = ('transaction_id', 'account_id')
    ordering = ('-created_at',)


if not getattr(settings, 'PAYME_DISABLE_ADMIN', False):
    admin.site.register(PaymeTransactions, PaymeTransactionsUI)
