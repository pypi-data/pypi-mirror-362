#!/usr/bin/env python3
"""
Logging utilities.
"""

import logging
from contextlib import contextmanager


@contextmanager
def temporary_console_logger(logger, level=logging.DEBUG):
    """
    Temporarily adds a console handler to the logger and adjusts its level.
    Args:
        logger: Logger instance.
        level: Temporary log level (e.g., logging.DEBUG, logging.INFO).
    """
    # Save previous values
    previous_level = logger.level

    # Configure the logger temporarily
    logger.setLevel(level)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    formatter = logging.Formatter("%(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    try:
        yield logger
    finally:
        # Restore previous state
        logger.removeHandler(console_handler)
        logger.setLevel(previous_level)
