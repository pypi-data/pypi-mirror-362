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
from mastapy._private.gears.gear_designs.conical import _1289

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LoadDistributionFactorMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LoadDistributionFactorMethods",)


class EnumWithSelectedValue_LoadDistributionFactorMethods(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_LoadDistributionFactorMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LoadDistributionFactorMethods' types.
    """

    __qualname__ = "LoadDistributionFactorMethods"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_LoadDistributionFactorMethods]",
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
        cls: "Type[EnumWithSelectedValue_LoadDistributionFactorMethods]",
    ) -> "_1289.LoadDistributionFactorMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1289.LoadDistributionFactorMethods
        """
        return _1289.LoadDistributionFactorMethods

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_LoadDistributionFactorMethods]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1289.LoadDistributionFactorMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1289.LoadDistributionFactorMethods":
        """mastapy.gears.gear_designs.conical.LoadDistributionFactorMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1289.LoadDistributionFactorMethods]":
        """List[mastapy.gears.gear_designs.conical.LoadDistributionFactorMethods]

        Note:
            This property is readonly.
        """
        return None
