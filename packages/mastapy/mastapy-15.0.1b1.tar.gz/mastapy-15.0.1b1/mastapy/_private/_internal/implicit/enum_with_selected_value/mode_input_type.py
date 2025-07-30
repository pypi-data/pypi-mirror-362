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
from mastapy._private.nodal_analysis import _81

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ModeInputType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ModeInputType",)


class EnumWithSelectedValue_ModeInputType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ModeInputType

    A specific implementation of 'EnumWithSelectedValue' for 'ModeInputType' types.
    """

    __qualname__ = "ModeInputType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ModeInputType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ModeInputType]",
    ) -> "_81.ModeInputType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _81.ModeInputType
        """
        return _81.ModeInputType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ModeInputType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _81.ModeInputType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_81.ModeInputType":
        """mastapy.nodal_analysis.ModeInputType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_81.ModeInputType]":
        """List[mastapy.nodal_analysis.ModeInputType]

        Note:
            This property is readonly.
        """
        return None
