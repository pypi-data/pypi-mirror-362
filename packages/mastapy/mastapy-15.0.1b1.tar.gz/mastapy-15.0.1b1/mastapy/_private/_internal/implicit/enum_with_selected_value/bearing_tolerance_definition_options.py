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
from mastapy._private.bearings.tolerances import _2107

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_BearingToleranceDefinitionOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BearingToleranceDefinitionOptions",)


class EnumWithSelectedValue_BearingToleranceDefinitionOptions(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_BearingToleranceDefinitionOptions

    A specific implementation of 'EnumWithSelectedValue' for 'BearingToleranceDefinitionOptions' types.
    """

    __qualname__ = "BearingToleranceDefinitionOptions"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_BearingToleranceDefinitionOptions]",
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
        cls: "Type[EnumWithSelectedValue_BearingToleranceDefinitionOptions]",
    ) -> "_2107.BearingToleranceDefinitionOptions":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2107.BearingToleranceDefinitionOptions
        """
        return _2107.BearingToleranceDefinitionOptions

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_BearingToleranceDefinitionOptions]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2107.BearingToleranceDefinitionOptions.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2107.BearingToleranceDefinitionOptions":
        """mastapy.bearings.tolerances.BearingToleranceDefinitionOptions

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2107.BearingToleranceDefinitionOptions]":
        """List[mastapy.bearings.tolerances.BearingToleranceDefinitionOptions]

        Note:
            This property is readonly.
        """
        return None
