from django.conf import settings
from django.core.checks import Error, register


@register()
def check_decimal_field_config(app_configs, **kwargs):
    errors = []

    max_digits = getattr(settings, "PAYME_TRANSACTION_AMOUNT_MAX_DIGITS", None)

    if max_digits is None:
        return errors
    if not isinstance(max_digits, int):
        errors.append(
            Error(
                "'PAYME_TRANSACTION_AMOUNT_MAX_DIGITS' in settings.py must be an integer.",
                id="payme.E001",
            )
        )

    return errors
