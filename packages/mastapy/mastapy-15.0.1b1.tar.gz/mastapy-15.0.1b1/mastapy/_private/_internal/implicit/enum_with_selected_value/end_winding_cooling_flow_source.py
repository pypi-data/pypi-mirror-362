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
from mastapy._private.electric_machines.thermal import _1466

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_EndWindingCoolingFlowSource")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_EndWindingCoolingFlowSource",)


class EnumWithSelectedValue_EndWindingCoolingFlowSource(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_EndWindingCoolingFlowSource

    A specific implementation of 'EnumWithSelectedValue' for 'EndWindingCoolingFlowSource' types.
    """

    __qualname__ = "EndWindingCoolingFlowSource"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_EndWindingCoolingFlowSource]",
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
        cls: "Type[EnumWithSelectedValue_EndWindingCoolingFlowSource]",
    ) -> "_1466.EndWindingCoolingFlowSource":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1466.EndWindingCoolingFlowSource
        """
        return _1466.EndWindingCoolingFlowSource

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_EndWindingCoolingFlowSource]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1466.EndWindingCoolingFlowSource.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1466.EndWindingCoolingFlowSource":
        """mastapy.electric_machines.thermal.EndWindingCoolingFlowSource

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1466.EndWindingCoolingFlowSource]":
        """List[mastapy.electric_machines.thermal.EndWindingCoolingFlowSource]

        Note:
            This property is readonly.
        """
        return None
