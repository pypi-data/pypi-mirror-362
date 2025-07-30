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
from mastapy._private.materials import _338

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_CylindricalGearRatingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_CylindricalGearRatingMethods",)


class EnumWithSelectedValue_CylindricalGearRatingMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_CylindricalGearRatingMethods

    A specific implementation of 'EnumWithSelectedValue' for 'CylindricalGearRatingMethods' types.
    """

    __qualname__ = "CylindricalGearRatingMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_CylindricalGearRatingMethods]",
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
        cls: "Type[EnumWithSelectedValue_CylindricalGearRatingMethods]",
    ) -> "_338.CylindricalGearRatingMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _338.CylindricalGearRatingMethods
        """
        return _338.CylindricalGearRatingMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_CylindricalGearRatingMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _338.CylindricalGearRatingMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_338.CylindricalGearRatingMethods":
        """mastapy.materials.CylindricalGearRatingMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_338.CylindricalGearRatingMethods]":
        """List[mastapy.materials.CylindricalGearRatingMethods]

        Note:
            This property is readonly.
        """
        return None
