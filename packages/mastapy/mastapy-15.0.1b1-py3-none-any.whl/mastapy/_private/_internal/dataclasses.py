"""Module for extended dataclass functionality."""

from __future__ import annotations

import sys
from copy import deepcopy
from dataclasses import FrozenInstanceError, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    T = TypeVar("T")


__all__ = ("extended_dataclass",)


def _extended_setattr(self: "T", name: str, value: "Any") -> None:
    cls = type(self)
    prop = getattr(cls, name, None)

    if isinstance(prop, property):
        prop.fset(self, value)
    else:
        raise FrozenInstanceError(f"cannot assign to field {name!r}") from None


def _extended_post_init(self: "T") -> None:
    type(self).__setattr__ = _extended_setattr

    if hasattr(self, "__real_post_init__"):
        self.__real_post_init__()


def extended_dataclass(
    *,
    init: bool = True,
    repr: bool = True,
    eq: bool = True,
    order: bool = False,
    unsafe_hash: bool = False,
    frozen: bool = False,
    match_args: bool = True,
    kw_only: bool = False,
    slots: bool = False,
    weakref_slot: bool = False,
) -> "Type[T]":
    """Extension to the built-in dataclass.

    The extended dataclass has backwards compatibility with our supported versions
    of Python as well as a custom implementation of frozen dataclasses that still allows
    the use of property setters.

    Args:
        init (bool, optional): A __init__ method will be generated. Default is True.
        repr (bool, optional): A __repr__ method will be generated. Default is True.
        eq (bool, optional): An __eq__ method will be generated. Default is True.
        order (bool, optional): __lt__, __le__, __gt__ and __ge__ methods will be
            generated. Default is False.
        unsafe_hash (bool, optional): If false, a __hash__ method will be generated.
            Default is False.
        frozen (bool, optional): Assigning to fields will be disabled. This
            does not apply to property setters. Default is False.
        match_args (bool, optional): A __match_args__ tuple will be generated. This
            functionality is disabled in Python<3.10. Default is True.
        kw_only (bool, optional): All fields will be marked as keyword only.
            This functionality is disabled in Python<3.10. Default is False.
        slots (bool, optional): A __slots__ attribute will be generated. This
            functionality is disabled in Python<3.10. Default is False.
        weakref_slot (bool, optional): A __weakref__ slot will be added. This
            functionality is disabled in Python<3.11. Default is False.

    Returns:
        Type[T]
    """
    kwargs = locals()
    kwargs = {key: kwargs[key] for key in dataclass.__kwdefaults__}

    if sys.version_info.major == 3 and sys.version_info.minor == 10:
        kwargs.pop("slots")

    def wrap(cls: "Type[T]") -> "Type[T]":
        result = dataclass(cls, **kwargs)

        if frozen:
            post_init_method = getattr(result, "__post_init__", None)

            if post_init_method is not None:
                result.__real_post_init__ = deepcopy(post_init_method)

            result.__post_init__ = _extended_post_init

        return result

    return wrap
