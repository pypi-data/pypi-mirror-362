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
from mastapy._private.utility.enums import _2021

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection",)


class EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection

    A specific implementation of 'EnumWithSelectedValue' for 'ThreeDViewContourOptionSecondSelection' types.
    """

    __qualname__ = "ThreeDViewContourOptionSecondSelection"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection]",
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
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection]",
    ) -> "_2021.ThreeDViewContourOptionSecondSelection":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2021.ThreeDViewContourOptionSecondSelection
        """
        return _2021.ThreeDViewContourOptionSecondSelection

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ThreeDViewContourOptionSecondSelection]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2021.ThreeDViewContourOptionSecondSelection.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2021.ThreeDViewContourOptionSecondSelection":
        """mastapy.utility.enums.ThreeDViewContourOptionSecondSelection

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2021.ThreeDViewContourOptionSecondSelection]":
        """List[mastapy.utility.enums.ThreeDViewContourOptionSecondSelection]

        Note:
            This property is readonly.
        """
        return None
