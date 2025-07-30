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
from mastapy._private.utility.cad_export import _2035

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DxfVersionWithName")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DxfVersionWithName",)


class EnumWithSelectedValue_DxfVersionWithName(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_DxfVersionWithName

    A specific implementation of 'EnumWithSelectedValue' for 'DxfVersionWithName' types.
    """

    __qualname__ = "DxfVersionWithName"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_DxfVersionWithName]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_DxfVersionWithName]",
    ) -> "_2035.DxfVersionWithName":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2035.DxfVersionWithName
        """
        return _2035.DxfVersionWithName

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_DxfVersionWithName]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2035.DxfVersionWithName.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2035.DxfVersionWithName":
        """mastapy.utility.cad_export.DxfVersionWithName

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2035.DxfVersionWithName]":
        """List[mastapy.utility.cad_export.DxfVersionWithName]

        Note:
            This property is readonly.
        """
        return None
