import logging

from rich.logging import RichHandler

_LOGGER_NAME = "zona"


def setup_logging(
    level: str = "INFO",
):
    logger = logging.getLogger(_LOGGER_NAME)
    logger.setLevel(level.upper())

    logger.propagate = False

    if not logger.handlers:
        handler = RichHandler(rich_tracebacks=True, show_path=False)
        handler.setLevel(level.upper())
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)


def get_logger(name: str = _LOGGER_NAME) -> logging.Logger:
    return logging.getLogger(name)
