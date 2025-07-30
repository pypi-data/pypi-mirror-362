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
from mastapy._private.nodal_analysis.varying_input_components import _104

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_SinglePointSelectionMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_SinglePointSelectionMethod",)


class EnumWithSelectedValue_SinglePointSelectionMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_SinglePointSelectionMethod

    A specific implementation of 'EnumWithSelectedValue' for 'SinglePointSelectionMethod' types.
    """

    __qualname__ = "SinglePointSelectionMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_SinglePointSelectionMethod]",
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
        cls: "Type[EnumWithSelectedValue_SinglePointSelectionMethod]",
    ) -> "_104.SinglePointSelectionMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _104.SinglePointSelectionMethod
        """
        return _104.SinglePointSelectionMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_SinglePointSelectionMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _104.SinglePointSelectionMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_104.SinglePointSelectionMethod":
        """mastapy.nodal_analysis.varying_input_components.SinglePointSelectionMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_104.SinglePointSelectionMethod]":
        """List[mastapy.nodal_analysis.varying_input_components.SinglePointSelectionMethod]

        Note:
            This property is readonly.
        """
        return None
