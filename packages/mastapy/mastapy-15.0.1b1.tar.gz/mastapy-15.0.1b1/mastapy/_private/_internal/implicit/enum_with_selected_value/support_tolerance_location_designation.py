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
from mastapy._private.bearings.tolerances import _2126

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_SupportToleranceLocationDesignation"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_SupportToleranceLocationDesignation",)


class EnumWithSelectedValue_SupportToleranceLocationDesignation(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_SupportToleranceLocationDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'SupportToleranceLocationDesignation' types.
    """

    __qualname__ = "SupportToleranceLocationDesignation"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_SupportToleranceLocationDesignation]",
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
        cls: "Type[EnumWithSelectedValue_SupportToleranceLocationDesignation]",
    ) -> "_2126.SupportToleranceLocationDesignation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2126.SupportToleranceLocationDesignation
        """
        return _2126.SupportToleranceLocationDesignation

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_SupportToleranceLocationDesignation]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2126.SupportToleranceLocationDesignation.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2126.SupportToleranceLocationDesignation":
        """mastapy.bearings.tolerances.SupportToleranceLocationDesignation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2126.SupportToleranceLocationDesignation]":
        """List[mastapy.bearings.tolerances.SupportToleranceLocationDesignation]

        Note:
            This property is readonly.
        """
        return None
