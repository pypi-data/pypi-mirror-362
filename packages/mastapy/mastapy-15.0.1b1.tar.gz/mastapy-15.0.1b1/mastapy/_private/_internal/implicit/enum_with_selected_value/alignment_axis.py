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
from mastapy._private.math_utility import _1675

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_AlignmentAxis")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_AlignmentAxis",)


class EnumWithSelectedValue_AlignmentAxis(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_AlignmentAxis

    A specific implementation of 'EnumWithSelectedValue' for 'AlignmentAxis' types.
    """

    __qualname__ = "AlignmentAxis"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_AlignmentAxis]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_AlignmentAxis]",
    ) -> "_1675.AlignmentAxis":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1675.AlignmentAxis
        """
        return _1675.AlignmentAxis

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_AlignmentAxis]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1675.AlignmentAxis.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1675.AlignmentAxis":
        """mastapy.math_utility.AlignmentAxis

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1675.AlignmentAxis]":
        """List[mastapy.math_utility.AlignmentAxis]

        Note:
            This property is readonly.
        """
        return None
