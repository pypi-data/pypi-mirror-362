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
from mastapy._private.materials.efficiency import _389

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_OilSealLossCalculationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_OilSealLossCalculationMethod",)


class EnumWithSelectedValue_OilSealLossCalculationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_OilSealLossCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'OilSealLossCalculationMethod' types.
    """

    __qualname__ = "OilSealLossCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_OilSealLossCalculationMethod]",
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
        cls: "Type[EnumWithSelectedValue_OilSealLossCalculationMethod]",
    ) -> "_389.OilSealLossCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _389.OilSealLossCalculationMethod
        """
        return _389.OilSealLossCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_OilSealLossCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _389.OilSealLossCalculationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_389.OilSealLossCalculationMethod":
        """mastapy.materials.efficiency.OilSealLossCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_389.OilSealLossCalculationMethod]":
        """List[mastapy.materials.efficiency.OilSealLossCalculationMethod]

        Note:
            This property is readonly.
        """
        return None
