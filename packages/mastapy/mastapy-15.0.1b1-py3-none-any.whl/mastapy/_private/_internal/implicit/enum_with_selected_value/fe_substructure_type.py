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
from mastapy._private.system_model.fe import _2610

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_FESubstructureType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_FESubstructureType",)


class EnumWithSelectedValue_FESubstructureType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_FESubstructureType

    A specific implementation of 'EnumWithSelectedValue' for 'FESubstructureType' types.
    """

    __qualname__ = "FESubstructureType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_FESubstructureType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_FESubstructureType]",
    ) -> "_2610.FESubstructureType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2610.FESubstructureType
        """
        return _2610.FESubstructureType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_FESubstructureType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2610.FESubstructureType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2610.FESubstructureType":
        """mastapy.system_model.fe.FESubstructureType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2610.FESubstructureType]":
        """List[mastapy.system_model.fe.FESubstructureType]

        Note:
            This property is readonly.
        """
        return None
