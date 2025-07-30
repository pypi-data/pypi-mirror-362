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
from mastapy._private.utility.model_validation import _1990

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_StatusItemSeverity")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_StatusItemSeverity",)


class EnumWithSelectedValue_StatusItemSeverity(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_StatusItemSeverity

    A specific implementation of 'EnumWithSelectedValue' for 'StatusItemSeverity' types.
    """

    __qualname__ = "StatusItemSeverity"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_StatusItemSeverity]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_StatusItemSeverity]",
    ) -> "_1990.StatusItemSeverity":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1990.StatusItemSeverity
        """
        return _1990.StatusItemSeverity

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_StatusItemSeverity]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1990.StatusItemSeverity.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1990.StatusItemSeverity":
        """mastapy.utility.model_validation.StatusItemSeverity

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1990.StatusItemSeverity]":
        """List[mastapy.utility.model_validation.StatusItemSeverity]

        Note:
            This property is readonly.
        """
        return None
