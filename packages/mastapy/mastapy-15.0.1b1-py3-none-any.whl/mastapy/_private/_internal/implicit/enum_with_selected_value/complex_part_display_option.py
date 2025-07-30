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
from mastapy._private.math_utility import _1679

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ComplexPartDisplayOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ComplexPartDisplayOption",)


class EnumWithSelectedValue_ComplexPartDisplayOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ComplexPartDisplayOption

    A specific implementation of 'EnumWithSelectedValue' for 'ComplexPartDisplayOption' types.
    """

    __qualname__ = "ComplexPartDisplayOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ComplexPartDisplayOption]",
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
        cls: "Type[EnumWithSelectedValue_ComplexPartDisplayOption]",
    ) -> "_1679.ComplexPartDisplayOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1679.ComplexPartDisplayOption
        """
        return _1679.ComplexPartDisplayOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ComplexPartDisplayOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1679.ComplexPartDisplayOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1679.ComplexPartDisplayOption":
        """mastapy.math_utility.ComplexPartDisplayOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1679.ComplexPartDisplayOption]":
        """List[mastapy.math_utility.ComplexPartDisplayOption]

        Note:
            This property is readonly.
        """
        return None
