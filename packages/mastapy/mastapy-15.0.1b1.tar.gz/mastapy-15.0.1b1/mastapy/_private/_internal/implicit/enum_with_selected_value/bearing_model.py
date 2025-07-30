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
from mastapy._private.bearings import _2080

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_BearingModel")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_BearingModel",)


class EnumWithSelectedValue_BearingModel(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_BearingModel

    A specific implementation of 'EnumWithSelectedValue' for 'BearingModel' types.
    """

    __qualname__ = "BearingModel"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_BearingModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_BearingModel]",
    ) -> "_2080.BearingModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2080.BearingModel
        """
        return _2080.BearingModel

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_BearingModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2080.BearingModel.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2080.BearingModel]":
        """List[mastapy.bearings.BearingModel]

        Note:
            This property is readonly.
        """
        return None
