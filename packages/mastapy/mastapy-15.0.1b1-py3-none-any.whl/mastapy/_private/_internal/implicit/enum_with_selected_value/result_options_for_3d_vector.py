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
from mastapy._private.math_utility import _1711

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ResultOptionsFor3DVector")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ResultOptionsFor3DVector",)


class EnumWithSelectedValue_ResultOptionsFor3DVector(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ResultOptionsFor3DVector

    A specific implementation of 'EnumWithSelectedValue' for 'ResultOptionsFor3DVector' types.
    """

    __qualname__ = "ResultOptionsFor3DVector"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ResultOptionsFor3DVector]",
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
        cls: "Type[EnumWithSelectedValue_ResultOptionsFor3DVector]",
    ) -> "_1711.ResultOptionsFor3DVector":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1711.ResultOptionsFor3DVector
        """
        return _1711.ResultOptionsFor3DVector

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ResultOptionsFor3DVector]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1711.ResultOptionsFor3DVector.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1711.ResultOptionsFor3DVector":
        """mastapy.math_utility.ResultOptionsFor3DVector

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1711.ResultOptionsFor3DVector]":
        """List[mastapy.math_utility.ResultOptionsFor3DVector]

        Note:
            This property is readonly.
        """
        return None
