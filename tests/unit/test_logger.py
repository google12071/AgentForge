"""Test logger module"""

from src.utils.logger import get_logger


def test_get_logger_returns_logger():
    """Test get_logger returns a valid logger"""
    logger = get_logger("test")

    assert logger is not None
    assert hasattr(logger, "info")
    assert hasattr(logger, "error")
    assert hasattr(logger, "debug")


def test_logger_can_log():
    """Test logger can log messages"""
    logger = get_logger("test")

    # These should not raise exceptions
    logger.info("Test info message")
    logger.debug("Test debug message")
    logger.warning("Test warning message")