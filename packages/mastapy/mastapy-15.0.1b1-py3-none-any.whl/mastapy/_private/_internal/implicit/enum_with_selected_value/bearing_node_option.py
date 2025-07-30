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
from mastapy._private.system_model.fe import _2584

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BearingNodeOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BearingNodeOption",)


class EnumWithSelectedValue_BearingNodeOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingNodeOption

    A specific implementation of 'EnumWithSelectedValue' for 'BearingNodeOption' types.
    """

    __qualname__ = "BearingNodeOption"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BearingNodeOption]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BearingNodeOption]",
    ) -> "_2584.BearingNodeOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2584.BearingNodeOption
        """
        return _2584.BearingNodeOption

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_BearingNodeOption]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2584.BearingNodeOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2584.BearingNodeOption":
        """mastapy.system_model.fe.BearingNodeOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2584.BearingNodeOption]":
        """List[mastapy.system_model.fe.BearingNodeOption]

        Note:
            This property is readonly.
        """
        return None
