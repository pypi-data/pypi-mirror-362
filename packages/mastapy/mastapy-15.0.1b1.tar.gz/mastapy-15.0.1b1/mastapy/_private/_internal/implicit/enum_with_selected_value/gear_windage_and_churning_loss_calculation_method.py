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
from mastapy._private.gears import _422

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod",)


class EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'GearWindageAndChurningLossCalculationMethod' types.
    """

    __qualname__ = "GearWindageAndChurningLossCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod]",
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
        cls: "Type[EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod]",
    ) -> "_422.GearWindageAndChurningLossCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _422.GearWindageAndChurningLossCalculationMethod
        """
        return _422.GearWindageAndChurningLossCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_GearWindageAndChurningLossCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _422.GearWindageAndChurningLossCalculationMethod.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_422.GearWindageAndChurningLossCalculationMethod":
        """mastapy.gears.GearWindageAndChurningLossCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_422.GearWindageAndChurningLossCalculationMethod]":
        """List[mastapy.gears.GearWindageAndChurningLossCalculationMethod]

        Note:
            This property is readonly.
        """
        return None
