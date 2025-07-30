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
from mastapy._private.bearings.bearing_designs.rolling import _2362

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum",)


class EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum

    A specific implementation of 'EnumWithSelectedValue' for 'FatigueLoadLimitCalculationMethodEnum' types.
    """

    __qualname__ = "FatigueLoadLimitCalculationMethodEnum"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum]",
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
        cls: "Type[EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum]",
    ) -> "_2362.FatigueLoadLimitCalculationMethodEnum":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2362.FatigueLoadLimitCalculationMethodEnum
        """
        return _2362.FatigueLoadLimitCalculationMethodEnum

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2362.FatigueLoadLimitCalculationMethodEnum.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2362.FatigueLoadLimitCalculationMethodEnum":
        """mastapy.bearings.bearing_designs.rolling.FatigueLoadLimitCalculationMethodEnum

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2362.FatigueLoadLimitCalculationMethodEnum]":
        """List[mastapy.bearings.bearing_designs.rolling.FatigueLoadLimitCalculationMethodEnum]

        Note:
            This property is readonly.
        """
        return None
