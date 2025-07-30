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
from mastapy._private.nodal_analysis.fe_export_utility import _245

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_BoundaryConditionType")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_BoundaryConditionType",)


class Overridable_BoundaryConditionType(mixins.OverridableMixin, Enum):
    """Overridable_BoundaryConditionType

    A specific implementation of 'Overridable' for 'BoundaryConditionType' types.
    """

    __qualname__ = "BoundaryConditionType"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_BoundaryConditionType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_BoundaryConditionType]",
    ) -> "_245.BoundaryConditionType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _245.BoundaryConditionType
        """
        return _245.BoundaryConditionType

    @classmethod
    def implicit_type(cls: "Type[Overridable_BoundaryConditionType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _245.BoundaryConditionType.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_245.BoundaryConditionType":
        """mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType

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
    def override_value(self: "Self") -> "_245.BoundaryConditionType":
        """mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_245.BoundaryConditionType":
        """mastapy.nodal_analysis.fe_export_utility.BoundaryConditionType

        Note:
            This property is readonly.
        """
        return None
