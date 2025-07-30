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
from mastapy._private.gears.gear_designs.cylindrical import _1184

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods",)


class EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods

    A specific implementation of 'EnumWithSelectedValue' for 'ScuffingCoefficientOfFrictionMethods' types.
    """

    __qualname__ = "ScuffingCoefficientOfFrictionMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods]",
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
        cls: "Type[EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods]",
    ) -> "_1184.ScuffingCoefficientOfFrictionMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1184.ScuffingCoefficientOfFrictionMethods
        """
        return _1184.ScuffingCoefficientOfFrictionMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ScuffingCoefficientOfFrictionMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1184.ScuffingCoefficientOfFrictionMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1184.ScuffingCoefficientOfFrictionMethods":
        """mastapy.gears.gear_designs.cylindrical.ScuffingCoefficientOfFrictionMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1184.ScuffingCoefficientOfFrictionMethods]":
        """List[mastapy.gears.gear_designs.cylindrical.ScuffingCoefficientOfFrictionMethods]

        Note:
            This property is readonly.
        """
        return None
