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
from mastapy._private.detailed_rigid_connectors.splines import _1589

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_PressureAngleTypes")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_PressureAngleTypes",)


class EnumWithSelectedValue_PressureAngleTypes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_PressureAngleTypes

    A specific implementation of 'EnumWithSelectedValue' for 'PressureAngleTypes' types.
    """

    __qualname__ = "PressureAngleTypes"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_PressureAngleTypes]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_PressureAngleTypes]",
    ) -> "_1589.PressureAngleTypes":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1589.PressureAngleTypes
        """
        return _1589.PressureAngleTypes

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_PressureAngleTypes]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1589.PressureAngleTypes.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1589.PressureAngleTypes":
        """mastapy.detailed_rigid_connectors.splines.PressureAngleTypes

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1589.PressureAngleTypes]":
        """List[mastapy.detailed_rigid_connectors.splines.PressureAngleTypes]

        Note:
            This property is readonly.
        """
        return None
