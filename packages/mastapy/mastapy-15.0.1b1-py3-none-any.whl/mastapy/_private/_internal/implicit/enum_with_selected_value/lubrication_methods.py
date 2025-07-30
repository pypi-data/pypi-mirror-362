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
from mastapy._private.gears import _425

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LubricationMethods")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LubricationMethods",)


class EnumWithSelectedValue_LubricationMethods(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LubricationMethods

    A specific implementation of 'EnumWithSelectedValue' for 'LubricationMethods' types.
    """

    __qualname__ = "LubricationMethods"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_LubricationMethods]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_LubricationMethods]",
    ) -> "_425.LubricationMethods":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _425.LubricationMethods
        """
        return _425.LubricationMethods

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_LubricationMethods]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _425.LubricationMethods.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_425.LubricationMethods":
        """mastapy.gears.LubricationMethods

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_425.LubricationMethods]":
        """List[mastapy.gears.LubricationMethods]

        Note:
            This property is readonly.
        """
        return None
