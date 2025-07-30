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
from mastapy._private.system_model.analyses_and_results.static_loads import _7686

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_AnalysisType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_AnalysisType",)


class EnumWithSelectedValue_AnalysisType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_AnalysisType

    A specific implementation of 'EnumWithSelectedValue' for 'AnalysisType' types.
    """

    __qualname__ = "AnalysisType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_AnalysisType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_AnalysisType]",
    ) -> "_7686.AnalysisType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7686.AnalysisType
        """
        return _7686.AnalysisType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_AnalysisType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7686.AnalysisType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_7686.AnalysisType":
        """mastapy.system_model.analyses_and_results.static_loads.AnalysisType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_7686.AnalysisType]":
        """List[mastapy.system_model.analyses_and_results.static_loads.AnalysisType]

        Note:
            This property is readonly.
        """
        return None
