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
from mastapy._private.gears.micro_geometry import _666

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LocationOfRootReliefEvaluation")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LocationOfRootReliefEvaluation",)


class EnumWithSelectedValue_LocationOfRootReliefEvaluation(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LocationOfRootReliefEvaluation

    A specific implementation of 'EnumWithSelectedValue' for 'LocationOfRootReliefEvaluation' types.
    """

    __qualname__ = "LocationOfRootReliefEvaluation"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LocationOfRootReliefEvaluation]",
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
        cls: "Type[EnumWithSelectedValue_LocationOfRootReliefEvaluation]",
    ) -> "_666.LocationOfRootReliefEvaluation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _666.LocationOfRootReliefEvaluation
        """
        return _666.LocationOfRootReliefEvaluation

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LocationOfRootReliefEvaluation]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _666.LocationOfRootReliefEvaluation.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_666.LocationOfRootReliefEvaluation":
        """mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_666.LocationOfRootReliefEvaluation]":
        """List[mastapy.gears.micro_geometry.LocationOfRootReliefEvaluation]

        Note:
            This property is readonly.
        """
        return None
