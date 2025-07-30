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
from mastapy._private.gears.gear_designs.cylindrical import _1181

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ResidualStressCalculationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ResidualStressCalculationMethod",)


class EnumWithSelectedValue_ResidualStressCalculationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ResidualStressCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ResidualStressCalculationMethod' types.
    """

    __qualname__ = "ResidualStressCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ResidualStressCalculationMethod]",
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
        cls: "Type[EnumWithSelectedValue_ResidualStressCalculationMethod]",
    ) -> "_1181.ResidualStressCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1181.ResidualStressCalculationMethod
        """
        return _1181.ResidualStressCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ResidualStressCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1181.ResidualStressCalculationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1181.ResidualStressCalculationMethod":
        """mastapy.gears.gear_designs.cylindrical.ResidualStressCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1181.ResidualStressCalculationMethod]":
        """List[mastapy.gears.gear_designs.cylindrical.ResidualStressCalculationMethod]

        Note:
            This property is readonly.
        """
        return None
