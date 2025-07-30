import logging


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    msg_format = "%(asctime)s %(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + msg_format + reset,
        logging.INFO: grey + msg_format + reset,
        logging.WARNING: yellow + msg_format + reset,
        logging.ERROR: red + msg_format + reset,
        logging.CRITICAL: bold_red + msg_format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(fmt=log_fmt, datefmt="%Y-%m-%d %I:%M:%S %p")
        return formatter.format(record)


def setup_logger(logger: logging.Logger = None, handler: logging.Handler = None) -> logging.Logger:
    """
    Set up the logger with the handler and formatter.
    :param logger: The logger to be set up. If None, the root logger is used.
    :param handler: The handler to be set up. If None, a StreamHandler is used with the CustomFormatter.
    """
    current_handler = handler
    if current_handler is None:
        current_handler = logging.StreamHandler()
        current_handler.setFormatter(CustomFormatter())
    current_logger = logger
    if current_logger is None:
        current_logger = logging.getLogger()
    current_logger.addHandler(current_handler)
    return current_logger
