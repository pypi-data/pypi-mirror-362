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
from mastapy._private.system_model.part_model.couplings import _2844

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_SplinePitchErrorInputType")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_SplinePitchErrorInputType",)


class Overridable_SplinePitchErrorInputType(mixins.OverridableMixin, Enum):
    """Overridable_SplinePitchErrorInputType

    A specific implementation of 'Overridable' for 'SplinePitchErrorInputType' types.
    """

    __qualname__ = "SplinePitchErrorInputType"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_SplinePitchErrorInputType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_SplinePitchErrorInputType]",
    ) -> "_2844.SplinePitchErrorInputType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2844.SplinePitchErrorInputType
        """
        return _2844.SplinePitchErrorInputType

    @classmethod
    def implicit_type(cls: "Type[Overridable_SplinePitchErrorInputType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2844.SplinePitchErrorInputType.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_2844.SplinePitchErrorInputType":
        """mastapy.system_model.part_model.couplings.SplinePitchErrorInputType

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
    def override_value(self: "Self") -> "_2844.SplinePitchErrorInputType":
        """mastapy.system_model.part_model.couplings.SplinePitchErrorInputType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_2844.SplinePitchErrorInputType":
        """mastapy.system_model.part_model.couplings.SplinePitchErrorInputType

        Note:
            This property is readonly.
        """
        return None
