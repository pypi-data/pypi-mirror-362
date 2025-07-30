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
from mastapy._private.electric_machines import _1384

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_DQAxisConvention")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_DQAxisConvention",)


class Overridable_DQAxisConvention(mixins.OverridableMixin, Enum):
    """Overridable_DQAxisConvention

    A specific implementation of 'Overridable' for 'DQAxisConvention' types.
    """

    __qualname__ = "DQAxisConvention"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_DQAxisConvention]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_DQAxisConvention]",
    ) -> "_1384.DQAxisConvention":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1384.DQAxisConvention
        """
        return _1384.DQAxisConvention

    @classmethod
    def implicit_type(cls: "Type[Overridable_DQAxisConvention]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1384.DQAxisConvention.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_1384.DQAxisConvention":
        """mastapy.electric_machines.DQAxisConvention

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
    def override_value(self: "Self") -> "_1384.DQAxisConvention":
        """mastapy.electric_machines.DQAxisConvention

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_1384.DQAxisConvention":
        """mastapy.electric_machines.DQAxisConvention

        Note:
            This property is readonly.
        """
        return None
