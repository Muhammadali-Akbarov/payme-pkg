from django.contrib import admin


from payme.models import PaymeTransactions


class PaymeTransactionsUI(admin.ModelAdmin):
    """
    Custom admin interface for PaymeTransactions model.
    """
    list_display = ('id', 'state', 'cancel_reason', 'created_at')
    list_filter = ('state', 'cancel_reason', 'created_at')
    search_fields = ('transaction_id', 'account__id')
    ordering = ('-created_at',)


admin.site.register(PaymeTransactions, PaymeTransactionsUI)
