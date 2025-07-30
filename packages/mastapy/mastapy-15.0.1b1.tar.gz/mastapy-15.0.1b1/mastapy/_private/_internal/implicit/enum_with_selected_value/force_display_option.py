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
from mastapy._private.electric_machines.harmonic_load_data import _1563

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ForceDisplayOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ForceDisplayOption",)


class EnumWithSelectedValue_ForceDisplayOption(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ForceDisplayOption

    A specific implementation of 'EnumWithSelectedValue' for 'ForceDisplayOption' types.
    """

    __qualname__ = "ForceDisplayOption"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ForceDisplayOption]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ForceDisplayOption]",
    ) -> "_1563.ForceDisplayOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1563.ForceDisplayOption
        """
        return _1563.ForceDisplayOption

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ForceDisplayOption]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1563.ForceDisplayOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1563.ForceDisplayOption":
        """mastapy.electric_machines.harmonic_load_data.ForceDisplayOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1563.ForceDisplayOption]":
        """List[mastapy.electric_machines.harmonic_load_data.ForceDisplayOption]

        Note:
            This property is readonly.
        """
        return None
