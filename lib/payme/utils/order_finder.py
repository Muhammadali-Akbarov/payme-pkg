from django.conf import settings
from django.db import models
from django.utils.module_loading import import_string


def _custom_order_model():
    """
    Get custom order model class from settings.

    Returns the custom order model class 
    defined in 'PAYME' or main settings.

    raise ImportError if both are undefined.
    """
    order_model_paths = []

    if hasattr(settings, 'ORDER_MODEL'):
        order_model_paths.append(settings.ORDER_MODEL)

    if hasattr(settings, 'PAYME'):
        order_model_paths.append(settings.PAYME.get('ORDER_MODEL'))

    for model_path in order_model_paths:
        try:
            return import_string(model_path)
        except (ImportError, AttributeError):
            pass

    raise ImportError


try:
    CUSTOM_ORDER = _custom_order_model()
except (ImportError, AttributeError):
    # pylint: disable=raise-missing-from
    raise NotImplementedError("Order model not implemented!")

if not isinstance(CUSTOM_ORDER, models.base.ModelBase):
    raise TypeError("The input must be an instance of models.Model class")

Order = CUSTOM_ORDER
