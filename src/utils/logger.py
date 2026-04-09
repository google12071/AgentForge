"""Logging module using Loguru"""

import sys
from loguru import logger
from pathlib import Path

from .config import settings


def get_logger(name: str = "agentforge") -> "logger":
    """Get configured logger instance

    Args:
        name: Logger name for identification

    Returns:
        Configured loguru logger instance
    """
    # Remove default handler
    logger.remove()

    # Add console handler
    logger.add(
        sys.stderr,
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
        colorize=True,
    )

    # Add file handler if log file is configured
    if settings.log_file:
        log_path = Path(settings.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        logger.add(
            log_path,
            level=settings.log_level,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name} - {message}",
            rotation="10 MB",
            retention="7 days",
            compression="zip",
        )

    return logger.bind(name=name)


# Default logger instance
default_logger = get_logger()