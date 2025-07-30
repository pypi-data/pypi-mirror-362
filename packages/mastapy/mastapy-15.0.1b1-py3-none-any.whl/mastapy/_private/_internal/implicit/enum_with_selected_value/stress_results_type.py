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
from mastapy._private.nodal_analysis import _93

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_StressResultsType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_StressResultsType",)


class EnumWithSelectedValue_StressResultsType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_StressResultsType

    A specific implementation of 'EnumWithSelectedValue' for 'StressResultsType' types.
    """

    __qualname__ = "StressResultsType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_StressResultsType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_StressResultsType]",
    ) -> "_93.StressResultsType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _93.StressResultsType
        """
        return _93.StressResultsType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_StressResultsType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _93.StressResultsType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_93.StressResultsType":
        """mastapy.nodal_analysis.StressResultsType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_93.StressResultsType]":
        """List[mastapy.nodal_analysis.StressResultsType]

        Note:
            This property is readonly.
        """
        return None
