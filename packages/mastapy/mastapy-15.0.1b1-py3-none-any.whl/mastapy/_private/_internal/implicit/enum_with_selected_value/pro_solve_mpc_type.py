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
from mastapy._private.fe_tools.vfx_tools.vfx_enums import _1361

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ProSolveMpcType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ProSolveMpcType",)


class EnumWithSelectedValue_ProSolveMpcType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ProSolveMpcType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveMpcType' types.
    """

    __qualname__ = "ProSolveMpcType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ProSolveMpcType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ProSolveMpcType]",
    ) -> "_1361.ProSolveMpcType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1361.ProSolveMpcType
        """
        return _1361.ProSolveMpcType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ProSolveMpcType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1361.ProSolveMpcType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1361.ProSolveMpcType":
        """mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveMpcType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1361.ProSolveMpcType]":
        """List[mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveMpcType]

        Note:
            This property is readonly.
        """
        return None
