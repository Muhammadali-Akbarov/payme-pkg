"""
Payme enumerations
"""
from enum import Enum


class Networks(str, Enum):
    """
    Payme networks
    """
    PROD_NET = "https://checkout.paycom.uz/api"
    TEST_NET = "https://checkout.test.paycom.uz/api"
