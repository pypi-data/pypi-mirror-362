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
from mastapy._private.system_model.fe import _2587

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ComponentOrientationOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ComponentOrientationOption",)


class EnumWithSelectedValue_ComponentOrientationOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ComponentOrientationOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComponentOrientationOption' types.
    """

    __qualname__ = "ComponentOrientationOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ComponentOrientationOption]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ComponentOrientationOption]",
    ) -> "_2587.ComponentOrientationOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2587.ComponentOrientationOption
        """
        return _2587.ComponentOrientationOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ComponentOrientationOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2587.ComponentOrientationOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2587.ComponentOrientationOption":
        """mastapy.system_model.fe.ComponentOrientationOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2587.ComponentOrientationOption]":
        """List[mastapy.system_model.fe.ComponentOrientationOption]

        Note:
            This property is readonly.
        """
        return None
