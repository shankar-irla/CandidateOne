"""
CandidateOne Logger Utility

Provides a centralized logger for the entire application.

Every module should import:

    from utils.logger import get_logger

"""

import logging
import os
from logging.handlers import RotatingFileHandler


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

LOG_DIRECTORY = "logs"
LOG_FILE = "candidateone.log"

DEFAULT_LEVEL = logging.INFO

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)-8s | "
    "%(name)s | "
    "%(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


# ---------------------------------------------------------
# Create log directory
# ---------------------------------------------------------

os.makedirs(LOG_DIRECTORY, exist_ok=True)


# ---------------------------------------------------------
# Logger Factory
# ---------------------------------------------------------

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger.

    Parameters
    ----------
    name : str
        Usually __name__ of the caller.

    Returns
    -------
    logging.Logger
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(DEFAULT_LEVEL)

    formatter = logging.Formatter(
        LOG_FORMAT,
        datefmt=DATE_FORMAT
    )

    # -----------------------------------------------------
    # Console Handler
    # -----------------------------------------------------

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # -----------------------------------------------------
    # File Handler
    # -----------------------------------------------------

    file_handler = RotatingFileHandler(
        filename=os.path.join(LOG_DIRECTORY, LOG_FILE),
        maxBytes=2 * 1024 * 1024,   # 2 MB
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger


# ---------------------------------------------------------
# Root Logger
# ---------------------------------------------------------

logger = get_logger("CandidateOne")