"""
Defines a custom Logger class for the Logcatter library.

This module is intended to hold the core configuration, such as the logger's name.
"""
import logging


class Logcat(logging.Logger):
    """
    A custom logger class that sets a default name and level.

    This class is designed to be the base for the application's logger,
    providing a consistent name ("logcat") across the library.

    Attributes:
        NAME (str): The static name for the logger.
    """
    NAME = "logcat"

    def __init__(self):
        """Initializes the Logcat logger with a default name and level."""
        super().__init__(name=self.NAME, level=logging.DEBUG)
