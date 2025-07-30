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
from mastapy._private.gears.micro_geometry import _667

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LocationOfTipReliefEvaluation")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LocationOfTipReliefEvaluation",)


class EnumWithSelectedValue_LocationOfTipReliefEvaluation(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LocationOfTipReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfTipReliefEvaluation' types.
    """

    __qualname__ = "LocationOfTipReliefEvaluation"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LocationOfTipReliefEvaluation]",
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
        cls: "Type[EnumWithSelectedValue_LocationOfTipReliefEvaluation]",
    ) -> "_667.LocationOfTipReliefEvaluation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _667.LocationOfTipReliefEvaluation
        """
        return _667.LocationOfTipReliefEvaluation

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LocationOfTipReliefEvaluation]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _667.LocationOfTipReliefEvaluation.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_667.LocationOfTipReliefEvaluation":
        """mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_667.LocationOfTipReliefEvaluation]":
        """List[mastapy.gears.micro_geometry.LocationOfTipReliefEvaluation]

        Note:
            This property is readonly.
        """
        return None
