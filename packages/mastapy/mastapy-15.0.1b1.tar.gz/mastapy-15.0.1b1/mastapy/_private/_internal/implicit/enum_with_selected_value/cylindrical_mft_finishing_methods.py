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
from mastapy._private.gears.manufacturing.cylindrical import _726

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CylindricalMftFinishingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CylindricalMftFinishingMethods",)


class EnumWithSelectedValue_CylindricalMftFinishingMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_CylindricalMftFinishingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalMftFinishingMethods' types.
    """

    __qualname__ = "CylindricalMftFinishingMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_CylindricalMftFinishingMethods]",
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
        cls: "Type[EnumWithSelectedValue_CylindricalMftFinishingMethods]",
    ) -> "_726.CylindricalMftFinishingMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _726.CylindricalMftFinishingMethods
        """
        return _726.CylindricalMftFinishingMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_CylindricalMftFinishingMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _726.CylindricalMftFinishingMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_726.CylindricalMftFinishingMethods":
        """mastapy.gears.manufacturing.cylindrical.CylindricalMftFinishingMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_726.CylindricalMftFinishingMethods]":
        """List[mastapy.gears.manufacturing.cylindrical.CylindricalMftFinishingMethods]

        Note:
            This property is readonly.
        """
        return None
