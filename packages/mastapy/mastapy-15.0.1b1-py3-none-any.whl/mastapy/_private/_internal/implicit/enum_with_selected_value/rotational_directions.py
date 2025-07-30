"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings import _2100

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_RotationalDirections")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_RotationalDirections",)


class EnumWithSelectedValue_RotationalDirections(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_RotationalDirections

    A specific implementation of 'EnumWithSelectedValue' for 'RotationalDirections' types.
    """

    __qualname__ = "RotationalDirections"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_RotationalDirections]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_RotationalDirections]",
    ) -> "_2100.RotationalDirections":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2100.RotationalDirections
        """
        return _2100.RotationalDirections

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_RotationalDirections]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2100.RotationalDirections.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2100.RotationalDirections":
        """mastapy.bearings.RotationalDirections

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2100.RotationalDirections]":
        """List[mastapy.bearings.RotationalDirections]

        Note:
            This property is readonly.
        """
        return None
