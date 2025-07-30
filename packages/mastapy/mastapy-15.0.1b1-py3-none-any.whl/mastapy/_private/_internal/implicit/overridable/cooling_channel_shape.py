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
from mastapy._private.electric_machines import _1378

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_CoolingChannelShape")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_CoolingChannelShape",)


class Overridable_CoolingChannelShape(mixins.OverridableMixin, Enum):
    """Overridable_CoolingChannelShape

    A specific implementation of 'Overridable' for 'CoolingChannelShape' types.
    """

    __qualname__ = "CoolingChannelShape"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_CoolingChannelShape]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_CoolingChannelShape]",
    ) -> "_1378.CoolingChannelShape":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1378.CoolingChannelShape
        """
        return _1378.CoolingChannelShape

    @classmethod
    def implicit_type(cls: "Type[Overridable_CoolingChannelShape]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1378.CoolingChannelShape.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_1378.CoolingChannelShape":
        """mastapy.electric_machines.CoolingChannelShape

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
    def override_value(self: "Self") -> "_1378.CoolingChannelShape":
        """mastapy.electric_machines.CoolingChannelShape

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_1378.CoolingChannelShape":
        """mastapy.electric_machines.CoolingChannelShape

        Note:
            This property is readonly.
        """
        return None
