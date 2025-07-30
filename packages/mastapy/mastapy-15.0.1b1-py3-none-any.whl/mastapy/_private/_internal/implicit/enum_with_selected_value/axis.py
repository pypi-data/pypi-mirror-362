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
from mastapy._private.math_utility import _1676

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_Axis")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_Axis",)


class EnumWithSelectedValue_Axis(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Axis

    A specific implementation of 'EnumWithSelectedValue' for 'Axis' types.
    """

    __qualname__ = "Axis"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_Axis]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls: "Type[EnumWithSelectedValue_Axis]") -> "_1676.Axis":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1676.Axis
        """
        return _1676.Axis

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_Axis]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1676.Axis.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1676.Axis":
        """mastapy.math_utility.Axis

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1676.Axis]":
        """List[mastapy.math_utility.Axis]

        Note:
            This property is readonly.
        """
        return None
