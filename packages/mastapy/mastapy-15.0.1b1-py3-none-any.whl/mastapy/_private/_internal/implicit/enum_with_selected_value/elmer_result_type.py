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
from mastapy._private.nodal_analysis.elmer import _255

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ElmerResultType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ElmerResultType",)


class EnumWithSelectedValue_ElmerResultType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ElmerResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ElmerResultType' types.
    """

    __qualname__ = "ElmerResultType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ElmerResultType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ElmerResultType]",
    ) -> "_255.ElmerResultType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _255.ElmerResultType
        """
        return _255.ElmerResultType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ElmerResultType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _255.ElmerResultType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_255.ElmerResultType":
        """mastapy.nodal_analysis.elmer.ElmerResultType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_255.ElmerResultType]":
        """List[mastapy.nodal_analysis.elmer.ElmerResultType]

        Note:
            This property is readonly.
        """
        return None
