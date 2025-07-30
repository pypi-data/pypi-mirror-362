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
from mastapy._private.bearings.bearing_results.rolling import _2173

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_BallBearingContactCalculation")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_BallBearingContactCalculation",)


class Overridable_BallBearingContactCalculation(mixins.OverridableMixin, Enum):
    """Overridable_BallBearingContactCalculation

    A specific implementation of 'Overridable' for 'BallBearingContactCalculation' types.
    """

    __qualname__ = "BallBearingContactCalculation"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_BallBearingContactCalculation]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_BallBearingContactCalculation]",
    ) -> "_2173.BallBearingContactCalculation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2173.BallBearingContactCalculation
        """
        return _2173.BallBearingContactCalculation

    @classmethod
    def implicit_type(cls: "Type[Overridable_BallBearingContactCalculation]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2173.BallBearingContactCalculation.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2173.BallBearingContactCalculation":
        """mastapy.bearings.bearing_results.rolling.BallBearingContactCalculation

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
    def override_value(self: "Self") -> "_2173.BallBearingContactCalculation":
        """mastapy.bearings.bearing_results.rolling.BallBearingContactCalculation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2173.BallBearingContactCalculation":
        """mastapy.bearings.bearing_results.rolling.BallBearingContactCalculation

        Note:
            This property is readonly.
        """
        return None
