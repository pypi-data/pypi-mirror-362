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
from mastapy._private.system_model.analyses_and_results.static_loads import _7792

_OVERRIDABLE = python_net_import("SMT.MastaAPI.Utility.Property", "Overridable")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Overridable_MeshStiffnessSource")


__docformat__ = "restructuredtext en"
__all__ = ("Overridable_MeshStiffnessSource",)


class Overridable_MeshStiffnessSource(mixins.OverridableMixin, Enum):
    """Overridable_MeshStiffnessSource

    A specific implementation of 'Overridable' for 'MeshStiffnessSource' types.
    """

    __qualname__ = "MeshStiffnessSource"

    @classmethod
    def wrapper_type(cls: "Type[Overridable_MeshStiffnessSource]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _OVERRIDABLE

    @classmethod
    def wrapped_type(
        cls: "Type[Overridable_MeshStiffnessSource]",
    ) -> "_7792.MeshStiffnessSource":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7792.MeshStiffnessSource
        """
        return _7792.MeshStiffnessSource

    @classmethod
    def implicit_type(cls: "Type[Overridable_MeshStiffnessSource]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7792.MeshStiffnessSource.type_()

    @property
    @exception_bridge
    def value(self: "Self") -> "_7792.MeshStiffnessSource":
        """mastapy.system_model.analyses_and_results.static_loads.MeshStiffnessSource

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
    def override_value(self: "Self") -> "_7792.MeshStiffnessSource":
        """mastapy.system_model.analyses_and_results.static_loads.MeshStiffnessSource

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def calculated_value(self: "Self") -> "_7792.MeshStiffnessSource":
        """mastapy.system_model.analyses_and_results.static_loads.MeshStiffnessSource

        Note:
            This property is readonly.
        """
        return None
