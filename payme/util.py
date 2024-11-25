from datetime import datetime


def time_to_payme(datatime) -> int:
    """
    Convert datetime object to Payme's datetime format.

    Payme's datetime format is in the format: YYYY-MM-DD HH:MM:SS.ssssss

    Args:
    datatime (datetime): The datetime object to convert.

    Returns:
    str: The datetime object in Payme's datetime format.
    """
    if not datatime:
        return 0

    return int(datatime.timestamp() * 1000)


def time_to_service(milliseconds: int) -> datetime:
    """
    Converts milliseconds since the epoch to a datetime object.
    """
    return datetime.fromtimestamp(milliseconds / 1000)
