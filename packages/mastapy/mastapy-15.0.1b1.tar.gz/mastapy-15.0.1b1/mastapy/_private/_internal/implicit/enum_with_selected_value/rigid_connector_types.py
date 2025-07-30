"""Implementations of 'EnumWithSelectedValue' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.couplings import _2837

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_RigidConnectorTypes")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_RigidConnectorTypes",)


class EnumWithSelectedValue_RigidConnectorTypes(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_RigidConnectorTypes

    A specific implementation of 'EnumWithSelectedValue' for 'RigidConnectorTypes' types.
    """

    __qualname__ = "RigidConnectorTypes"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_RigidConnectorTypes]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_RigidConnectorTypes]",
    ) -> "_2837.RigidConnectorTypes":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2837.RigidConnectorTypes
        """
        return _2837.RigidConnectorTypes

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_RigidConnectorTypes]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2837.RigidConnectorTypes.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2837.RigidConnectorTypes":
        """mastapy.system_model.part_model.couplings.RigidConnectorTypes

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2837.RigidConnectorTypes]":
        """List[mastapy.system_model.part_model.couplings.RigidConnectorTypes]

        Note:
            This property is readonly.
        """
        return None
