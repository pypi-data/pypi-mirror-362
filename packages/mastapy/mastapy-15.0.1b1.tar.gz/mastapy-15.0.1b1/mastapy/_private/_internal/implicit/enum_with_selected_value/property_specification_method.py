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
from mastapy._private.utility.enums import _2017

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_PropertySpecificationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_PropertySpecificationMethod",)


class EnumWithSelectedValue_PropertySpecificationMethod(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_PropertySpecificationMethod

    A specific implementation of 'EnumWithSelectedValue' for 'PropertySpecificationMethod' types.
    """

    __qualname__ = "PropertySpecificationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_PropertySpecificationMethod]",
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
        cls: "Type[EnumWithSelectedValue_PropertySpecificationMethod]",
    ) -> "_2017.PropertySpecificationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2017.PropertySpecificationMethod
        """
        return _2017.PropertySpecificationMethod

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_PropertySpecificationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2017.PropertySpecificationMethod.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2017.PropertySpecificationMethod":
        """mastapy.utility.enums.PropertySpecificationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2017.PropertySpecificationMethod]":
        """List[mastapy.utility.enums.PropertySpecificationMethod]

        Note:
            This property is readonly.
        """
        return None
