from django.apps import AppConfig


class PaymeConfig(AppConfig):
    """
    PaymeConfig AppConfig \
        That is used to configure the payme application with django settings.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payme'
