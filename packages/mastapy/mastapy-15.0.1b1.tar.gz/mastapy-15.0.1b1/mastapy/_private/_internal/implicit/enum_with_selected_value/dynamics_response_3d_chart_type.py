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
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4896

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DynamicsResponse3DChartType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DynamicsResponse3DChartType",)


class EnumWithSelectedValue_DynamicsResponse3DChartType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DynamicsResponse3DChartType

    A specific implementation of 'EnumWithSelectedValue' for 'DynamicsResponse3DChartType' types.
    """

    __qualname__ = "DynamicsResponse3DChartType"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_DynamicsResponse3DChartType]",
    ) -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_DynamicsResponse3DChartType]",
    ) -> "_4896.DynamicsResponse3DChartType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _4896.DynamicsResponse3DChartType
        """
        return _4896.DynamicsResponse3DChartType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_DynamicsResponse3DChartType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _4896.DynamicsResponse3DChartType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_4896.DynamicsResponse3DChartType":
        """mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponse3DChartType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_4896.DynamicsResponse3DChartType]":
        """List[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponse3DChartType]

        Note:
            This property is readonly.
        """
        return None
