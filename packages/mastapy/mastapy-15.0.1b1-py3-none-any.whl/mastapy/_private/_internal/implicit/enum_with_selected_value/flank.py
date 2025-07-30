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
from mastapy._private.gears.manufacturing.cylindrical import _730

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_Flank")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_Flank",)


class EnumWithSelectedValue_Flank(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Flank

    A specific implementation of 'EnumWithSelectedValue' for 'Flank' types.
    """

    __qualname__ = "Flank"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_Flank]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls: "Type[EnumWithSelectedValue_Flank]") -> "_730.Flank":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _730.Flank
        """
        return _730.Flank

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_Flank]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _730.Flank.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_730.Flank":
        """mastapy.gears.manufacturing.cylindrical.Flank

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_730.Flank]":
        """List[mastapy.gears.manufacturing.cylindrical.Flank]

        Note:
            This property is readonly.
        """
        return None
