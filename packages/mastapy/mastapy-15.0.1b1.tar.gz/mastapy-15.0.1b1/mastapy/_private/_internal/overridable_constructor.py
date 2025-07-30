"""Module containing helpful methods for overridables."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Tuple, TypeVar, Union

    T = TypeVar("T")


def _unpack_overridable(v: "Union[Tuple[T, bool], T]") -> "Tuple[T, bool]":
    if hasattr(v, "__iter__"):
        if len(v) == 1:
            return v, True

        if len(v) > 2:
            raise TypeError("Overridable tuple must be of length 2.")

        value, is_overridden = v

        try:
            is_overridden = bool(is_overridden)
        except ValueError:
            return v, True

        return value, is_overridden

    return v, True


def overridable(override_value: "T", is_overridden: bool = True) -> "Tuple[T, bool]":
    """Create overridable values.

    You can use this method to set whether an overridable property should use the
    overridden value or not. Alternatively, you can just pass a tuple to the
    overridable property.

    Args:
        override_value (T): value to override the property with
        is_overridden (bool, optional): whether the property should use
            the overridden value. Default is True.

    Returns:
        Tuple[T, bool]

    Examples:
        >>> my_gear_set.mass = overridable(100.0, False)
        >>> my_gear_set.mass = 100.0, False

    """
    return override_value, is_overridden
