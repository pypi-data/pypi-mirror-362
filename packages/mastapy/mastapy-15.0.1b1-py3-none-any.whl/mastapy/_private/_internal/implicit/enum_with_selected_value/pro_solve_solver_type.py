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
from mastapy._private.fe_tools.vfx_tools.vfx_enums import _1362

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ProSolveSolverType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ProSolveSolverType",)


class EnumWithSelectedValue_ProSolveSolverType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ProSolveSolverType

    A specific implementation of 'EnumWithSelectedValue' for 'ProSolveSolverType' types.
    """

    __qualname__ = "ProSolveSolverType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ProSolveSolverType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ProSolveSolverType]",
    ) -> "_1362.ProSolveSolverType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1362.ProSolveSolverType
        """
        return _1362.ProSolveSolverType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ProSolveSolverType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1362.ProSolveSolverType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1362.ProSolveSolverType":
        """mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveSolverType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1362.ProSolveSolverType]":
        """List[mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveSolverType]

        Note:
            This property is readonly.
        """
        return None
