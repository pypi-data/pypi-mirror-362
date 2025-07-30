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
from mastapy._private.nodal_analysis import _97

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ValueInputOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ValueInputOption",)


class EnumWithSelectedValue_ValueInputOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ValueInputOption

    A specific implementation of 'EnumWithSelectedValue' for 'ValueInputOption' types.
    """

    __qualname__ = "ValueInputOption"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ValueInputOption]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ValueInputOption]",
    ) -> "_97.ValueInputOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _97.ValueInputOption
        """
        return _97.ValueInputOption

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ValueInputOption]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _97.ValueInputOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_97.ValueInputOption":
        """mastapy.nodal_analysis.ValueInputOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_97.ValueInputOption]":
        """List[mastapy.nodal_analysis.ValueInputOption]

        Note:
            This property is readonly.
        """
        return None
