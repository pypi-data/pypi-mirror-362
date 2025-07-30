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
from mastapy._private.bearings.bearing_results import _2169

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_RaceAxialMountingType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_RaceAxialMountingType",)


class EnumWithSelectedValue_RaceAxialMountingType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_RaceAxialMountingType

    A specific implementation of 'EnumWithSelectedValue' for 'RaceAxialMountingType' types.
    """

    __qualname__ = "RaceAxialMountingType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_RaceAxialMountingType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_RaceAxialMountingType]",
    ) -> "_2169.RaceAxialMountingType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2169.RaceAxialMountingType
        """
        return _2169.RaceAxialMountingType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_RaceAxialMountingType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2169.RaceAxialMountingType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2169.RaceAxialMountingType":
        """mastapy.bearings.bearing_results.RaceAxialMountingType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2169.RaceAxialMountingType]":
        """List[mastapy.bearings.bearing_results.RaceAxialMountingType]

        Note:
            This property is readonly.
        """
        return None
