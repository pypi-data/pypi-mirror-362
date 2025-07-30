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
from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _761,
)

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ActiveProcessMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ActiveProcessMethod",)


class EnumWithSelectedValue_ActiveProcessMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ActiveProcessMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ActiveProcessMethod' types.
    """

    __qualname__ = "ActiveProcessMethod"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ActiveProcessMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ActiveProcessMethod]",
    ) -> "_761.ActiveProcessMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _761.ActiveProcessMethod
        """
        return _761.ActiveProcessMethod

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ActiveProcessMethod]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _761.ActiveProcessMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_761.ActiveProcessMethod":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.ActiveProcessMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_761.ActiveProcessMethod]":
        """List[mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.ActiveProcessMethod]

        Note:
            This property is readonly.
        """
        return None
