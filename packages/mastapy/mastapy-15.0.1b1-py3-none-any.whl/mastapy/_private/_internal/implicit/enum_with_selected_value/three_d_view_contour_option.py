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
from mastapy._private.utility.enums import _2019

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ThreeDViewContourOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ThreeDViewContourOption",)


class EnumWithSelectedValue_ThreeDViewContourOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ThreeDViewContourOption

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOption' types.
    """

    __qualname__ = "ThreeDViewContourOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOption]",
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
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOption]",
    ) -> "_2019.ThreeDViewContourOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2019.ThreeDViewContourOption
        """
        return _2019.ThreeDViewContourOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2019.ThreeDViewContourOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2019.ThreeDViewContourOption":
        """mastapy.utility.enums.ThreeDViewContourOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2019.ThreeDViewContourOption]":
        """List[mastapy.utility.enums.ThreeDViewContourOption]

        Note:
            This property is readonly.
        """
        return None
