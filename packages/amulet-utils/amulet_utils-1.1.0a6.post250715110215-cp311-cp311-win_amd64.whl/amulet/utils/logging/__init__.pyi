from __future__ import annotations

import amulet.utils.signal

from . import _logging

__all__ = [
    "get_logger",
    "get_min_log_level",
    "register_default_log_handler",
    "set_min_log_level",
    "unregister_default_log_handler",
]

def get_logger() -> amulet.utils.signal.Signal[int, str]:
    """
    Get the logger signal.
    This is emitted with the message and its level every time a message is logged.
    """

def get_min_log_level() -> int:
    """
    Get the maximum message level that will be logged.
    Registered handlers may be more strict.
    Thread safe.
    """

def register_default_log_handler() -> None:
    """
    Register the default log handler.
    This is registered by default with a log level of 20.
    Thread safe.
    """

def set_min_log_level(level: int) -> None:
    """
    Set the maximum message level that will be logged.
    Registered handlers may be more strict.
    Thread safe.
    """

def unregister_default_log_handler() -> None:
    """
    Unregister the default log handler.
    Thread safe.
    """
