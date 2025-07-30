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
from mastapy._private.nodal_analysis import _56

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BarModelExportType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BarModelExportType",)


class EnumWithSelectedValue_BarModelExportType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BarModelExportType

    A specific implementation of 'EnumWithSelectedValue' for 'BarModelExportType' types.
    """

    __qualname__ = "BarModelExportType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BarModelExportType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BarModelExportType]",
    ) -> "_56.BarModelExportType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _56.BarModelExportType
        """
        return _56.BarModelExportType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_BarModelExportType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _56.BarModelExportType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_56.BarModelExportType":
        """mastapy.nodal_analysis.BarModelExportType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_56.BarModelExportType]":
        """List[mastapy.nodal_analysis.BarModelExportType]

        Note:
            This property is readonly.
        """
        return None
