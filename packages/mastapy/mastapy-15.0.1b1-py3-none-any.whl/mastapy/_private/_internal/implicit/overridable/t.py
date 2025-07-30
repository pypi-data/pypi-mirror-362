"""Implementations of 'Overridable' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Generic, TypeVar

from mastapy._private._internal import constructor, mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type

    Self = TypeVar("Self", bound="Overridable_T")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_T",)
T = TypeVar("T")


class Overridable_T(Generic[T], mixins.OverridableMixin):
    """Overridable_T

    A specific implementation of 'Overridable' for 'T' types.
    """

    __qualname__ = "T"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        object.__setattr__(self, "wrapped", instance_to_wrap.Value)
        object.__setattr__(self, "enclosing", instance_to_wrap)

    @classmethod
    def wrapper_type(cls: "Type[Overridable_T]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def implicit_type(cls: "Type[Overridable_T]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return T

    @property
    @exception_bridge
    def value(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "Value")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "Overridden")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def override_value(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "OverrideValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "T":
        """T

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "CalculatedValue")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)
