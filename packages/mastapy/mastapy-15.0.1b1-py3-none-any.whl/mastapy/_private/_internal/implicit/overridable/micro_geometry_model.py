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
from mastapy._private.gears import _427

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_MicroGeometryModel")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_MicroGeometryModel",)


class Overridable_MicroGeometryModel(mixins.OverridableMixin, Enum):
    """Overridable_MicroGeometryModel

    A specific implementation of 'Overridable' for 'MicroGeometryModel' types.
    """

    __qualname__ = "MicroGeometryModel"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_MicroGeometryModel]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_MicroGeometryModel]",
    ) -> "_427.MicroGeometryModel":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _427.MicroGeometryModel
        """
        return _427.MicroGeometryModel

    @classmethod
    def implicit_type(cls: "Type[Overridable_MicroGeometryModel]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _427.MicroGeometryModel.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_427.MicroGeometryModel":
        """mastapy.gears.MicroGeometryModel

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
    def override_value(self: "Self") -> "_427.MicroGeometryModel":
        """mastapy.gears.MicroGeometryModel

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_427.MicroGeometryModel":
        """mastapy.gears.MicroGeometryModel

        Note:
            This property is readonly.
        """
        return None
