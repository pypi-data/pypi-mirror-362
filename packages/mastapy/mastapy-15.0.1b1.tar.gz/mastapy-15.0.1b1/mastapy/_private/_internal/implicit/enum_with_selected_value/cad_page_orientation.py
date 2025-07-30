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
from mastapy._private.utility.report import _1940

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CadPageOrientation")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CadPageOrientation",)


class EnumWithSelectedValue_CadPageOrientation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_CadPageOrientation

    A specific implementation of 'EnumWithSelectedValue' for 'CadPageOrientation' types.
    """

    __qualname__ = "CadPageOrientation"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_CadPageOrientation]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_CadPageOrientation]",
    ) -> "_1940.CadPageOrientation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1940.CadPageOrientation
        """
        return _1940.CadPageOrientation

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_CadPageOrientation]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1940.CadPageOrientation.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1940.CadPageOrientation":
        """mastapy.utility.report.CadPageOrientation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1940.CadPageOrientation]":
        """List[mastapy.utility.report.CadPageOrientation]

        Note:
            This property is readonly.
        """
        return None
