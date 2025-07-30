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
from mastapy._private.nodal_analysis.nodal_entities import _137

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ShearAreaFactorMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ShearAreaFactorMethod",)


class EnumWithSelectedValue_ShearAreaFactorMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ShearAreaFactorMethod

    A specific implementation of 'EnumWithSelectedValue' for 'ShearAreaFactorMethod' types.
    """

    __qualname__ = "ShearAreaFactorMethod"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ShearAreaFactorMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ShearAreaFactorMethod]",
    ) -> "_137.ShearAreaFactorMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _137.ShearAreaFactorMethod
        """
        return _137.ShearAreaFactorMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ShearAreaFactorMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _137.ShearAreaFactorMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_137.ShearAreaFactorMethod":
        """mastapy.nodal_analysis.nodal_entities.ShearAreaFactorMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_137.ShearAreaFactorMethod]":
        """List[mastapy.nodal_analysis.nodal_entities.ShearAreaFactorMethod]

        Note:
            This property is readonly.
        """
        return None
