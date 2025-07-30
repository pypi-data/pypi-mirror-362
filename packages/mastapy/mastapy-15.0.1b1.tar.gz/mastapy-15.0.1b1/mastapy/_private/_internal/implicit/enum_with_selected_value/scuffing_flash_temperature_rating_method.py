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
from mastapy._private.gears.rating.cylindrical import _572

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod",)


class EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingFlashTemperatureRatingMethod' types.
    """

    __qualname__ = "ScuffingFlashTemperatureRatingMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod]",
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
        cls: "Type[EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod]",
    ) -> "_572.ScuffingFlashTemperatureRatingMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _572.ScuffingFlashTemperatureRatingMethod
        """
        return _572.ScuffingFlashTemperatureRatingMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ScuffingFlashTemperatureRatingMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _572.ScuffingFlashTemperatureRatingMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_572.ScuffingFlashTemperatureRatingMethod":
        """mastapy.gears.rating.cylindrical.ScuffingFlashTemperatureRatingMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_572.ScuffingFlashTemperatureRatingMethod]":
        """List[mastapy.gears.rating.cylindrical.ScuffingFlashTemperatureRatingMethod]

        Note:
            This property is readonly.
        """
        return None
