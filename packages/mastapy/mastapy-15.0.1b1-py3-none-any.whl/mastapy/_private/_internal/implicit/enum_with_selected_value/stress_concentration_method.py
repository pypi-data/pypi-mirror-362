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
from mastapy._private.bearings.bearing_results.rolling.iso_rating_results import _2318

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_StressConcentrationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_StressConcentrationMethod",)


class EnumWithSelectedValue_StressConcentrationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_StressConcentrationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'StressConcentrationMethod' types.
    """

    __qualname__ = "StressConcentrationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_StressConcentrationMethod]",
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
        cls: "Type[EnumWithSelectedValue_StressConcentrationMethod]",
    ) -> "_2318.StressConcentrationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2318.StressConcentrationMethod
        """
        return _2318.StressConcentrationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_StressConcentrationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2318.StressConcentrationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2318.StressConcentrationMethod":
        """mastapy.bearings.bearing_results.rolling.iso_rating_results.StressConcentrationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2318.StressConcentrationMethod]":
        """List[mastapy.bearings.bearing_results.rolling.iso_rating_results.StressConcentrationMethod]

        Note:
            This property is readonly.
        """
        return None
