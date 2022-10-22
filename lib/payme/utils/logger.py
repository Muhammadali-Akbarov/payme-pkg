import logging


logger = logging.getLogger('django')


def logged(logged_message: str, logged_type: str = "debug") -> None:
    """Use this function to logging.

    :param log_message: string -> log message
    :param _type: string -> log type choises ("info, error, warning, debug...")
        default: _type -> debug
    """
    if logged_type == 'info':
        logger.info(logged_message)
    if logged_type == "warning":
        logger.warning(logged_message)
    if logged_type == "debug":
        logger.debug(logged_message)
    if logged_type == "error":
        logger.error(logged_message)
    if logged_type == "critical":
        logger.critical(logged_message)

    if logged_type not in ['warning', 'error', 'debug', 'critical']:
        logger.debug(logged_message)
