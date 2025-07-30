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
from mastapy._private.system_model.part_model.gears import _2780

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ProfileToothDrawingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ProfileToothDrawingMethod",)


class EnumWithSelectedValue_ProfileToothDrawingMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ProfileToothDrawingMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ProfileToothDrawingMethod' types.
    """

    __qualname__ = "ProfileToothDrawingMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ProfileToothDrawingMethod]",
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
        cls: "Type[EnumWithSelectedValue_ProfileToothDrawingMethod]",
    ) -> "_2780.ProfileToothDrawingMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2780.ProfileToothDrawingMethod
        """
        return _2780.ProfileToothDrawingMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ProfileToothDrawingMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2780.ProfileToothDrawingMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2780.ProfileToothDrawingMethod":
        """mastapy.system_model.part_model.gears.ProfileToothDrawingMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2780.ProfileToothDrawingMethod]":
        """List[mastapy.system_model.part_model.gears.ProfileToothDrawingMethod]

        Note:
            This property is readonly.
        """
        return None
