from django.utils.timezone import datetime as dt
from django.utils.timezone import make_aware


def make_aware_datetime(start_date: int, end_date: int):
    """
    Convert Unix timestamps to aware datetimes.

    :param start_date: Unix timestamp (milliseconds)
    :param end_date: Unix timestamp (milliseconds)

    :return: A tuple of two aware datetimes
    """
    return map(
        lambda timestamp: make_aware(
            dt.fromtimestamp(
                timestamp / 1000
            )
        ),
        [start_date, end_date]
    )
