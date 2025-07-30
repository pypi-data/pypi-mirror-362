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
from mastapy._private.utility import _1781

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LoadCaseOverrideOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LoadCaseOverrideOption",)


class EnumWithSelectedValue_LoadCaseOverrideOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LoadCaseOverrideOption

    A specific implementation of 'EnumWithSelectedValue' for 'LoadCaseOverrideOption' types.
    """

    __qualname__ = "LoadCaseOverrideOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LoadCaseOverrideOption]",
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
        cls: "Type[EnumWithSelectedValue_LoadCaseOverrideOption]",
    ) -> "_1781.LoadCaseOverrideOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1781.LoadCaseOverrideOption
        """
        return _1781.LoadCaseOverrideOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LoadCaseOverrideOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1781.LoadCaseOverrideOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1781.LoadCaseOverrideOption":
        """mastapy.utility.LoadCaseOverrideOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1781.LoadCaseOverrideOption]":
        """List[mastapy.utility.LoadCaseOverrideOption]

        Note:
            This property is readonly.
        """
        return None
