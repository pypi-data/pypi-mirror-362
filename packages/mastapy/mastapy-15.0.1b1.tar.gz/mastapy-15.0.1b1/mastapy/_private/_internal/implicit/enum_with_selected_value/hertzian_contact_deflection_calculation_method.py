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
from mastapy._private.math_utility.hertzian_contact import _1758

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod",)


class EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'HertzianContactDeflectionCalculationMethod' types.
    """

    __qualname__ = "HertzianContactDeflectionCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod]",
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
        cls: "Type[EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod]",
    ) -> "_1758.HertzianContactDeflectionCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1758.HertzianContactDeflectionCalculationMethod
        """
        return _1758.HertzianContactDeflectionCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_HertzianContactDeflectionCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1758.HertzianContactDeflectionCalculationMethod.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_1758.HertzianContactDeflectionCalculationMethod":
        """mastapy.math_utility.hertzian_contact.HertzianContactDeflectionCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_1758.HertzianContactDeflectionCalculationMethod]":
        """List[mastapy.math_utility.hertzian_contact.HertzianContactDeflectionCalculationMethod]

        Note:
            This property is readonly.
        """
        return None
