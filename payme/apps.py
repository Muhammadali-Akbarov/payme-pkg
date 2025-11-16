from django.apps import AppConfig
from django.conf import settings

from payme.licensing import validate_api_key


class PaymeConfig(AppConfig):
    """Payme app config."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'payme'

    def ready(self):
        license_key = getattr(settings, "PAYTECH_API_KEY", None)
        validate_api_key(license_key)
