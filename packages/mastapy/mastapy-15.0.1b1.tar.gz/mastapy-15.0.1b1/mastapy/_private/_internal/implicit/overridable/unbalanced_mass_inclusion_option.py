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
from mastapy._private.system_model.part_model import _2710

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_UnbalancedMassInclusionOption")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_UnbalancedMassInclusionOption",)


class Overridable_UnbalancedMassInclusionOption(mixins.OverridableMixin, Enum):
    """Overridable_UnbalancedMassInclusionOption

    A specific implementation of 'Overridable' for 'UnbalancedMassInclusionOption' types.
    """

    __qualname__ = "UnbalancedMassInclusionOption"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_UnbalancedMassInclusionOption]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_UnbalancedMassInclusionOption]",
    ) -> "_2710.UnbalancedMassInclusionOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2710.UnbalancedMassInclusionOption
        """
        return _2710.UnbalancedMassInclusionOption

    @classmethod
    def implicit_type(cls: "Type[Overridable_UnbalancedMassInclusionOption]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2710.UnbalancedMassInclusionOption.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2710.UnbalancedMassInclusionOption":
        """mastapy.system_model.part_model.UnbalancedMassInclusionOption

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
    def override_value(self: "Self") -> "_2710.UnbalancedMassInclusionOption":
        """mastapy.system_model.part_model.UnbalancedMassInclusionOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2710.UnbalancedMassInclusionOption":
        """mastapy.system_model.part_model.UnbalancedMassInclusionOption

        Note:
            This property is readonly.
        """
        return None
