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
from mastapy._private.bearings import _2074

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod",)


class EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'BasicStaticLoadRatingCalculationMethod' types.
    """

    __qualname__ = "BasicStaticLoadRatingCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod]",
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
        cls: "Type[EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod]",
    ) -> "_2074.BasicStaticLoadRatingCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2074.BasicStaticLoadRatingCalculationMethod
        """
        return _2074.BasicStaticLoadRatingCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2074.BasicStaticLoadRatingCalculationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2074.BasicStaticLoadRatingCalculationMethod":
        """mastapy.bearings.BasicStaticLoadRatingCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2074.BasicStaticLoadRatingCalculationMethod]":
        """List[mastapy.bearings.BasicStaticLoadRatingCalculationMethod]

        Note:
            This property is readonly.
        """
        return None
