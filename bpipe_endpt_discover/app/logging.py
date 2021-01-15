"""
Abstracts away the stdlib logging to offer consistent logging to the application.
"""
import logging
import os
from typing import Union

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
FORMAT = "%(asctime)-15s %(levelname)s %(message)s"
logging.basicConfig(format=FORMAT, level=logging.getLevelName(LOG_LEVEL))


def get_logger(name: str, level: Union[str, int] = LOG_LEVEL) -> logging.Logger:
    """Produces a new logger with the application logging parameter preset.

    Args:
        name (str): [description]
        level (Union[str, int], optional): [description]. Defaults to LOG_LEVEL.

    Returns:
        logging.Logger: [description]
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.getLevelName(level))

    return logger
