"""Module for handling deprecation or obsoletion."""

from __future__ import annotations

import functools
import warnings


class ObsoleteException(Exception):
    """Simple exception for obsolete methods."""


def deprecated(alternative: str = ""):
    """Mark a method as deprecated.

    Args:
        alternative (str, optional): A simple message describing the
            alternative implementation to the deprecated method. Default is
            an empty string (no alternative message.)

    Note:
        This decorator produces a warning.
    """

    def _deprecated_decorator(func):
        @functools.wraps(func)
        def _deprecated(*args, **kwargs):
            message = f'The method "{func.__name__}" has been deprecated.'

            if alternative:
                message += f" {alternative}"

            warnings.warn(message, category=DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return _deprecated

    return _deprecated_decorator


def obsolete(alternative: str = ""):
    """Mark a method as obsolete.

    Args:
        alternative (str, optional): A simple message describing the
            alternative implementation to the obsoleted method. Default is
            an empty string (no alternative message.)

    Note:
        This decorator produces an exception.
    """

    def _obsolete_decorator(func):
        @functools.wraps(func)
        def _obsolete(*args, **kwargs):
            message = f'The method "{func.__name__}" has been made obsolete.'

            if alternative:
                message += f" {alternative}"

            raise ObsoleteException(message) from None

        return _obsolete

    return _obsolete_decorator
