"""This module provides a simple configuration for a Python logger.

It includes functionality to:
- Set up a logger with a console handler to output logs to the console.
- Optionally add a file handler to output logs to a specified log file.
- Customize the logging level to control the verbosity of log messages.

The `setup_logger` function is the main entry point, allowing users to create a configured
logger for their application. The example usage within the `__main__` block demonstrates
how to log messages at different logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL).


Copyright (c) 2024 Neil Schneider
"""

import logging
import sys
from pathlib import Path


# Configure the logger
def setup_logger(
    name: str,
    log_file: str | Path | None = None,
    level: int = logging.INFO,
) -> logging.Logger:
    """Sets up a logger with a console handler and an optional file handler.

    Args:
        name (str): The name of the logger.
        log_file (str, optional): The file path for logging output. If None, no file logging is set.
            Defaults to None.
        level (int, optional): The logging level (e.g., logging.DEBUG, logging.INFO).
            Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Formatter: Include time, name, log level, and the message
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Console handler: logs to the console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler: logs to a file if a file is specified
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    logger_ex = setup_logger('my_logger', log_file='example_log.log', level=logging.DEBUG)

    def _example_use() -> None:
        """Demonstrates the usage of the logger by logging messages at different levels."""
        logger_ex.debug('This is a debug message')
        logger_ex.info('This is an info message')
        logger_ex.warning('This is a warning message')
        logger_ex.error('This is an error message')
        logger_ex.critical('This is a critical message')
