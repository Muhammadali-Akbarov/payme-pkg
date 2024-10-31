from functools import wraps
from datetime import datetime
from typing import get_type_hints


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


def input_type_checker(func):
    """
    input type checker decorator helps to
    validate the input types of the function before executing it.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        Get the type hints of the function
        """
        hints = get_type_hints(func)

        all_args = kwargs.copy()
        all_args.update(zip(func.__code__.co_varnames, args))

        for arg_name, arg_type in hints.items():
            if arg_name in all_args and not isinstance(all_args[arg_name], arg_type): # noqa
                raise TypeError(
                    f"Argument '{arg_name}' in {func.__name__} must be of type {arg_type.__name__}, "  # noqa
                    f"but got {type(all_args[arg_name]).__name__}."
                )
        return func(*args, **kwargs)
    return wrapper
