"""
Provides a static, Android Logcat-style logging interface.

This module offers a simple, zero-configuration facade over Python's standard
logging module, designed to be instantly familiar to Android developers.
"""

import logging

from logcatter.formatter import LogFormatter
from logcatter.logcat import Logcat


class Log:
    """
    A static utility class that provides an Android Logcat-like logging interface.

    This class is not meant to be instantiated. It offers a set of static methods
    (e.g., `d`, `i`, `w`, `e`) that wrap the standard Python `logging` module
    to provide a simple, zero-configuration logging experience. It automatically
    configures a logger that outputs messages in a format similar to Android's
    Logcat, including automatic tagging with the calling filename.
    """

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL

    @staticmethod
    def getLogger() -> logging.Logger:
        """
        Retrieves the singleton logger instance for the application.

        On the first call, it initializes the logger with a `StreamHandler` and
        the custom `LogFormatter`. Subsequent calls return the same logger instance
        without adding more handlers, preventing duplicate log messages.

        Returns:
            logging.Logger: The configured logger instance.
        """
        logger = logging.getLogger(Logcat.NAME)
        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setFormatter(LogFormatter())
            logger.addHandler(handler)
        return logger

    @staticmethod
    def setLevel(level: int | str):
        """
        Sets the logging level for the application's logger.

        Messages with a severity lower than `level` will be ignored.

        Args:
            level (int | str): The minimum level of severity to log.
                Can be an integer constant (e.g., `logging.INFO`) or its string
                representation (e.g., "INFO").
        """
        Log.getLogger().setLevel(level)

    @staticmethod
    def d(msg: str, *args, **kwargs):
        """
        Logs a message with the DEBUG level.

        Args:
            msg (str): The message to be logged.
            *args: Arguments to be merged into `msg` using string formatting.
            **kwargs: Other keyword arguments for the underlying logger.
        """
        Log.getLogger().debug(msg, *args, stacklevel=2, **kwargs)

    @staticmethod
    def i(msg: str, *args, **kwargs):
        """
        Logs a message with the INFO level.

        Args:
            msg (str): The message to be logged.
            *args: Arguments to be merged into `msg` using string formatting.
            **kwargs: Other keyword arguments for the underlying logger.
        """
        Log.getLogger().info(msg, *args, stacklevel=2, **kwargs)

    @staticmethod
    def w(msg: str, *args, **kwargs):
        """
        Logs a message with the WARNING level.

        Args:
            msg (str): The message to be logged.
            *args: Arguments to be merged into `msg` using string formatting.
            **kwargs: Other keyword arguments for the underlying logger.
        """
        Log.getLogger().warning(msg, *args, stacklevel=2, **kwargs)

    @staticmethod
    def e(
            msg: str,
            *args,
            e: object | None = None,
            s: bool = False,
            **kwargs,
    ):
        """
        Logs a message with the ERROR level.

        This method includes special parameters for logging exception and stack information.

        Args:
            msg (str): The message to be logged.
            *args: Arguments to be merged into `msg` using string formatting.
            e (object | None, optional): Exception information to add to the log.
                Can be an exception object or `True` to capture the current exception.
                Defaults to None. Corresponds to the `exc_info` parameter.
            s (bool, optional): If True, adds stack information to the log.
                Defaults to False. Corresponds to the `stack_info` parameter.
            **kwargs: Other keyword arguments for the underlying logger.
        """
        Log.getLogger().error(
            msg,
            *args,
            stacklevel=2,
            exc_info=e,
            stack_info=s,
            **kwargs,
        )

    @staticmethod
    def f(
            msg: str,
            *args,
            e: object | None = None,
            s: bool = False,
            **kwargs,
    ):
        """
        Logs a message with the CRITICAL level.

        This method includes special parameters for logging exception and stack information.

        Args:
            msg (str): The message to be logged.
            *args: Arguments to be merged into `msg` using string formatting.
            e (object | None, optional): Exception information to add to the log.
                Can be an exception object or `True` to capture the current exception.
                Defaults to None. Corresponds to the `exc_info` parameter.
            s (bool, optional): If True, adds stack information to the log.
                Defaults to False. Corresponds to the `stack_info` parameter.
            **kwargs: Other keyword arguments for the underlying logger.
        """
        Log.getLogger().critical(
            msg,
            *args,
            stacklevel=2,
            exc_info=e,
            stack_info=s,
            **kwargs,
        )
