"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2368

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_HeightSeries")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_HeightSeries",)


class Overridable_HeightSeries(mixins.OverridableMixin, Enum):
    """Overridable_HeightSeries

    A specific implementation of 'Overridable' for 'HeightSeries' types.
    """

    __qualname__ = "HeightSeries"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_HeightSeries]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(cls: "Type[Overridable_HeightSeries]") -> "_2368.HeightSeries":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2368.HeightSeries
        """
        return _2368.HeightSeries

    @classmethod
    def implicit_type(cls: "Type[Overridable_HeightSeries]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2368.HeightSeries.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2368.HeightSeries":
        """mastapy.bearings.bearing_designs.rolling.HeightSeries

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def override_value(self: "Self") -> "_2368.HeightSeries":
        """mastapy.bearings.bearing_designs.rolling.HeightSeries

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2368.HeightSeries":
        """mastapy.bearings.bearing_designs.rolling.HeightSeries

        Note:
            This property is readonly.
        """
        return None
