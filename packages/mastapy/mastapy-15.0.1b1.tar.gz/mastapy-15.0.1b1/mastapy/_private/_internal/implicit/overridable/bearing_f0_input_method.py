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
from mastapy._private.system_model.part_model import _2665

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_BearingF0InputMethod")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_BearingF0InputMethod",)


class Overridable_BearingF0InputMethod(mixins.OverridableMixin, Enum):
    """Overridable_BearingF0InputMethod

    A specific implementation of 'Overridable' for 'BearingF0InputMethod' types.
    """

    __qualname__ = "BearingF0InputMethod"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_BearingF0InputMethod]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_BearingF0InputMethod]",
    ) -> "_2665.BearingF0InputMethod":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2665.BearingF0InputMethod
        """
        return _2665.BearingF0InputMethod

    @classmethod
    def implicit_type(cls: "Type[Overridable_BearingF0InputMethod]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2665.BearingF0InputMethod.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2665.BearingF0InputMethod":
        """mastapy.system_model.part_model.BearingF0InputMethod

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
    def override_value(self: "Self") -> "_2665.BearingF0InputMethod":
        """mastapy.system_model.part_model.BearingF0InputMethod

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2665.BearingF0InputMethod":
        """mastapy.system_model.part_model.BearingF0InputMethod

        Note:
            This property is readonly.
        """
        return None
