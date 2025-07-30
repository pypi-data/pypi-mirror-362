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
from mastapy._private.nodal_analysis.dev_tools_analyses import _288

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_RigidCouplingType")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_RigidCouplingType",)


class Overridable_RigidCouplingType(mixins.OverridableMixin, Enum):
    """Overridable_RigidCouplingType

    A specific implementation of 'Overridable' for 'RigidCouplingType' types.
    """

    __qualname__ = "RigidCouplingType"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_RigidCouplingType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_RigidCouplingType]",
    ) -> "_288.RigidCouplingType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _288.RigidCouplingType
        """
        return _288.RigidCouplingType

    @classmethod
    def implicit_type(cls: "Type[Overridable_RigidCouplingType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _288.RigidCouplingType.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_288.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

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
    def override_value(self: "Self") -> "_288.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_288.RigidCouplingType":
        """mastapy.nodal_analysis.dev_tools_analyses.RigidCouplingType

        Note:
            This property is readonly.
        """
        return None
