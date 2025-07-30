"""enum_with_selected_value_runtime.

This module holds methods for creating mastapy's EnumWithSelectedValue
type. We have to do this quite differently in Python compared to the original
C
present in mastapy._private._internal.implicit.enum_with_selected_value.
"""

from __future__ import annotations

import functools

from mastapy._private._internal import constructor, conversion
from mastapy._private._internal.python_net import python_net_import

ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)


__docformat__ = "restructuredtext en"
__all__ = ("create",)


def _selected_value(self):
    type_ = constructor.new_from_mastapy_class(type(self))
    value = conversion.pn_to_mp_enum(self.enclosing.SelectedValue, type_)
    return value if value else None


def _available_values(self, enum_type):
    int_iter = conversion.pn_to_mp_objects_in_iterable(
        self.enclosing.AvailableValues, int
    )
    return list(map(enum_type, int_iter))


def create(pn_enum, enum_type):
    """Create an altered enum with additional data and methods present.

    Mimics EnumWithSelectedValue from C
    because we can't use the custom constructor logic we need inside of
    a subclass of enum's constructor.

    Args:
        pn_enum: PythonNet enum
        enum_type: the enum_type to create

    Returns:
        an enum of type enum_type (with modifications)
    """
    enum_type.selected_value = property(_selected_value)

    available_values_partial = functools.partial(_available_values, enum_type=enum_type)
    enum_type.available_values = property(available_values_partial)

    wrapped_value = pn_enum.SelectedValue
    enum_value = enum_type(int(wrapped_value))

    enum_value.__dict__["enclosing"] = pn_enum
    enum_value.__dict__["wrapped"] = wrapped_value

    return enum_value
