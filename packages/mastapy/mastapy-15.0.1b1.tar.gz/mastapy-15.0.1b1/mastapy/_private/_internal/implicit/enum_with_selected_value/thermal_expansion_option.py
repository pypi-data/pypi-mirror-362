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
from mastapy._private.system_model.fe import _2636

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ThermalExpansionOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ThermalExpansionOption",)


class EnumWithSelectedValue_ThermalExpansionOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ThermalExpansionOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThermalExpansionOption' types.
    """

    __qualname__ = "ThermalExpansionOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ThermalExpansionOption]",
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
        cls: "Type[EnumWithSelectedValue_ThermalExpansionOption]",
    ) -> "_2636.ThermalExpansionOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2636.ThermalExpansionOption
        """
        return _2636.ThermalExpansionOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ThermalExpansionOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2636.ThermalExpansionOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2636.ThermalExpansionOption":
        """mastapy.system_model.fe.ThermalExpansionOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2636.ThermalExpansionOption]":
        """List[mastapy.system_model.fe.ThermalExpansionOption]

        Note:
            This property is readonly.
        """
        return None
