"""Create an overridable enum."""

from __future__ import annotations

import functools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from enum import Enum
    from typing import Any, Type, TypeVar

    from mastapy._private._internal import mixins

    TEnum = TypeVar("TEnum", bound=Enum)


__docformat__ = "restructuredtext en"
__all__ = ("create",)


def _value(self: "mixins.OverridableMixin", enum_type: "Type[TEnum]") -> "TEnum":
    temp = self.enclosing.Value

    if temp is None:
        return enum_type(0)

    return enum_type(int(temp))


def _overridden(self: "mixins.OverridableMixin") -> bool:
    temp = self.enclosing.Overridden

    if temp is None:
        return False

    return temp


def _override_value(
    self: "mixins.OverridableMixin", enum_type: "Type[TEnum]"
) -> "TEnum":
    temp = self.enclosing.OverrideValue

    if temp is None:
        return enum_type(0)

    return enum_type(int(temp))


def _calculated_value(
    self: "mixins.OverridableMixin", enum_type: "Type[TEnum]"
) -> "TEnum":
    temp = self.enclosing.CalculatedValue

    if temp is None:
        return enum_type(0)

    return enum_type(int(temp))


def create(pn_enum: "Any", enum_type: "Type[TEnum]") -> "TEnum":
    """Create an altered enum with additional data and methods present.

    Args:
        pn_enum (Any): Python.NET enum.
        enum_type (Type[TEnum]): the enum_type to create.

    Returns:
        TEnum
    """
    enum_type.value = property(functools.partial(_value, enum_type=enum_type))
    enum_type.overridden = property(_overridden)
    enum_type.override_value = property(
        functools.partial(_override_value, enum_type=enum_type)
    )
    enum_type.calculated_value = property(
        functools.partial(_calculated_value, enum_type=enum_type)
    )

    wrapped_value = pn_enum.Value
    enum_value = enum_type(int(wrapped_value))

    enum_value.__dict__["enclosing"] = pn_enum
    enum_value.__dict__["wrapped"] = wrapped_value

    return enum_value
