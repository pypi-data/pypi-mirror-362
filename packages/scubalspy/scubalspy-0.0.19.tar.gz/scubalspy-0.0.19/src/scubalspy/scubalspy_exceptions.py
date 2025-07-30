"""
This module contains the exceptions raised by the Scubalspy framework.
"""

class ScubalspyException(Exception):
    """
    Exceptions raised by the Scubalspy framework.
    """

    def __init__(self, message: str):
        """
        Initializes the exception with the given message.
        """
        super().__init__(message)