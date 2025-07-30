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
from mastapy._private.utility.model_validation import _1987

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_Severity")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_Severity",)


class EnumWithSelectedValue_Severity(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_Severity

    A specific implementation of 'EnumWithSelectedValue' for 'Severity' types.
    """

    __qualname__ = "Severity"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_Severity]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(cls: "Type[EnumWithSelectedValue_Severity]") -> "_1987.Severity":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1987.Severity
        """
        return _1987.Severity

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_Severity]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1987.Severity.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1987.Severity":
        """mastapy.utility.model_validation.Severity

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1987.Severity]":
        """List[mastapy.utility.model_validation.Severity]

        Note:
            This property is readonly.
        """
        return None
