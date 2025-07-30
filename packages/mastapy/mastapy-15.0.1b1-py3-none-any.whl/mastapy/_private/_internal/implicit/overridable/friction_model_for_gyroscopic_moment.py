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
from mastapy._private.bearings.bearing_results.rolling import _2179

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_FrictionModelForGyroscopicMoment")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_FrictionModelForGyroscopicMoment",)


class Overridable_FrictionModelForGyroscopicMoment(mixins.OverridableMixin, Enum):
    """Overridable_FrictionModelForGyroscopicMoment

    A specific implementation of 'Overridable' for 'FrictionModelForGyroscopicMoment' types.
    """

    __qualname__ = "FrictionModelForGyroscopicMoment"

    @classmethod
    def wrapper_type(
        cls: "Type[Overridable_FrictionModelForGyroscopicMoment]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_FrictionModelForGyroscopicMoment]",
    ) -> "_2179.FrictionModelForGyroscopicMoment":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2179.FrictionModelForGyroscopicMoment
        """
        return _2179.FrictionModelForGyroscopicMoment

    @classmethod
    def implicit_type(
        cls: "Type[Overridable_FrictionModelForGyroscopicMoment]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2179.FrictionModelForGyroscopicMoment.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2179.FrictionModelForGyroscopicMoment":
        """mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment

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
    def override_value(self: "Self") -> "_2179.FrictionModelForGyroscopicMoment":
        """mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2179.FrictionModelForGyroscopicMoment":
        """mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment

        Note:
            This property is readonly.
        """
        return None
