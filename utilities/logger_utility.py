"""
logger_utility.py
------------------
Single, reusable logger factory used by every module in the framework.

Why this exists:
    Without a centralized logger, every module would configure its own
    handlers/formatters, causing duplicate log lines, inconsistent formats,
    and scattered log files. `get_logger()` guarantees one consistent
    configuration across the entire framework.

Usage:
    from utilities.logger_utility import get_logger
    log = get_logger(__name__)
    log.info("Something happened")
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

from constants.constants import LOGS_DIR, TIMESTAMP_FORMAT
from config.config_reader import config_reader

_LOG_FILE_NAME = f"execution_{datetime.now().strftime(TIMESTAMP_FORMAT)}.log"
_LOG_FILE_PATH = os.path.join(LOGS_DIR, _LOG_FILE_NAME)

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_initialized = False


def _initialize_root_logger() -> None:
    """Configures the root logger exactly once per test run."""
    global _initialized
    if _initialized:
        return

    os.makedirs(LOGS_DIR, exist_ok=True)

    level_name = config_reader.get_log_level().upper()
    level = getattr(logging, level_name, logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    # Rotating file handler: keeps log files from growing unbounded
    file_handler = RotatingFileHandler(
        _LOG_FILE_PATH, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)

    # Console handler for real-time feedback during local runs
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    _initialized = True


def get_logger(name: str) -> logging.Logger:
    """
    Returns a named logger configured with the framework's standard
    handlers/formatters.

    Args:
        name: Typically `__name__` of the calling module.

    Returns:
        Configured `logging.Logger` instance.
    """
    _initialize_root_logger()
    return logging.getLogger(name)


def get_current_log_file() -> str:
    """Returns the absolute path of the log file used in this run."""
    return _LOG_FILE_PATH
