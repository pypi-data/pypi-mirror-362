import logging
import sys
from typing import Optional


def configure_logging(logger: logging.Logger, level: Optional[int] = None) -> None:
    """
    Configure logger with stdout and stderr handlers.

    :param logger: Logger instance to configure
    :param level: Logging level (e.g., logging.INFO, logging.DEBUG). If None, defaults to INFO.
    """
    if level is not None:
        logger.setLevel(level)
        logger.debug(f"Set logger level to {logging.getLevelName(level)}")

    logger.handlers.clear()
    logger.debug(f"Cleared existing handlers for {logger.name}")

    # Stdout handler for INFO and below
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
    )
    stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
    logger.addHandler(stdout_handler)
    logger.debug(f"Added stdout StreamHandler with level DEBUG")

    # Stderr handler for WARNING and above
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setLevel(logging.WARNING)
    stderr_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
    )
    logger.addHandler(stderr_handler)
    logger.debug(f"Added stderr StreamHandler with level WARNING")
