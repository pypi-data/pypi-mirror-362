"""Logger."""
import logging
import sys
from logging import Logger


def setup_logger() -> Logger:
    """Setup the logger."""
    log_format = logging.Formatter("[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s")
    log_level = logging.DEBUG
    logger = logging.getLogger("t_vault")
    if logger.hasHandlers():
        logger.handlers = []
    logger.setLevel(log_level)
    logger.propagate = False

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)
    handler.setFormatter(log_format)
    logger.addHandler(handler)

    return logger


logger = setup_logger()
