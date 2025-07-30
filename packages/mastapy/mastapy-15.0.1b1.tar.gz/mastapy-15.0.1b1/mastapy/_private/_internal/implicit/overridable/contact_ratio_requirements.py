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
from mastapy._private.gears import _411

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_ContactRatioRequirements")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_ContactRatioRequirements",)


class Overridable_ContactRatioRequirements(mixins.OverridableMixin, Enum):
    """Overridable_ContactRatioRequirements

    A specific implementation of 'Overridable' for 'ContactRatioRequirements' types.
    """

    __qualname__ = "ContactRatioRequirements"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_ContactRatioRequirements]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_ContactRatioRequirements]",
    ) -> "_411.ContactRatioRequirements":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _411.ContactRatioRequirements
        """
        return _411.ContactRatioRequirements

    @classmethod
    def implicit_type(cls: "Type[Overridable_ContactRatioRequirements]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _411.ContactRatioRequirements.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_411.ContactRatioRequirements":
        """mastapy.gears.ContactRatioRequirements

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
    def override_value(self: "Self") -> "_411.ContactRatioRequirements":
        """mastapy.gears.ContactRatioRequirements

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_411.ContactRatioRequirements":
        """mastapy.gears.ContactRatioRequirements

        Note:
            This property is readonly.
        """
        return None
