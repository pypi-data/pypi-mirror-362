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
from mastapy._private.shafts import _48

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_SurfaceFinishes")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_SurfaceFinishes",)


class EnumWithSelectedValue_SurfaceFinishes(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_SurfaceFinishes

    A specific implementation of 'EnumWithSelectedValue' for 'SurfaceFinishes' types.
    """

    __qualname__ = "SurfaceFinishes"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_SurfaceFinishes]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_SurfaceFinishes]",
    ) -> "_48.SurfaceFinishes":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _48.SurfaceFinishes
        """
        return _48.SurfaceFinishes

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_SurfaceFinishes]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _48.SurfaceFinishes.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_48.SurfaceFinishes":
        """mastapy.shafts.SurfaceFinishes

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_48.SurfaceFinishes]":
        """List[mastapy.shafts.SurfaceFinishes]

        Note:
            This property is readonly.
        """
        return None
