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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4897

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DynamicsResponseType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DynamicsResponseType",)


class EnumWithSelectedValue_DynamicsResponseType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DynamicsResponseType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponseType' types.
    """

    __qualname__ = "DynamicsResponseType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_DynamicsResponseType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_DynamicsResponseType]",
    ) -> "_4897.DynamicsResponseType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _4897.DynamicsResponseType
        """
        return _4897.DynamicsResponseType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_DynamicsResponseType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _4897.DynamicsResponseType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_4897.DynamicsResponseType":
        """mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponseType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_4897.DynamicsResponseType]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponseType]

        Note:
            This property is readonly.
        """
        return None
