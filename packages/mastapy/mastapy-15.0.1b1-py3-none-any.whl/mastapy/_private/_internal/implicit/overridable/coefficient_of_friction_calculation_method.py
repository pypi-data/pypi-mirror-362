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
from mastapy._private.gears import _408

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_CoefficientOfFrictionCalculationMethod")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_CoefficientOfFrictionCalculationMethod",)


class Overridable_CoefficientOfFrictionCalculationMethod(mixins.OverridableMixin, Enum):
    """Overridable_CoefficientOfFrictionCalculationMethod

    A specific implementation of 'Overridable' for 'CoefficientOfFrictionCalculationMethod' types.
    """

    __qualname__ = "CoefficientOfFrictionCalculationMethod"

    @classmethod
    def wrapper_type(
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
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
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
    ) -> "_408.CoefficientOfFrictionCalculationMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _408.CoefficientOfFrictionCalculationMethod
        """
        return _408.CoefficientOfFrictionCalculationMethod

    @classmethod
    def implicit_type(
        cls: "Type[Overridable_CoefficientOfFrictionCalculationMethod]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _408.CoefficientOfFrictionCalculationMethod.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_408.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

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
    def override_value(self: "Self") -> "_408.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_408.CoefficientOfFrictionCalculationMethod":
        """mastapy.gears.CoefficientOfFrictionCalculationMethod

        Note:
            This property is readonly.
        """
        return None
