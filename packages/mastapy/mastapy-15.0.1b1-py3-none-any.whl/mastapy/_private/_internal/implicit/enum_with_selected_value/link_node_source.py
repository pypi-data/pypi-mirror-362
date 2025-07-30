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
from mastapy._private.system_model.fe import _2623

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_LinkNodeSource")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_LinkNodeSource",)


class EnumWithSelectedValue_LinkNodeSource(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_LinkNodeSource

    A specific implementation of 'EnumWithSelectedValue' for 'LinkNodeSource' types.
    """

    __qualname__ = "LinkNodeSource"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_LinkNodeSource]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_LinkNodeSource]",
    ) -> "_2623.LinkNodeSource":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2623.LinkNodeSource
        """
        return _2623.LinkNodeSource

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_LinkNodeSource]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2623.LinkNodeSource.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2623.LinkNodeSource":
        """mastapy.system_model.fe.LinkNodeSource

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2623.LinkNodeSource]":
        """List[mastapy.system_model.fe.LinkNodeSource]

        Note:
            This property is readonly.
        """
        return None
