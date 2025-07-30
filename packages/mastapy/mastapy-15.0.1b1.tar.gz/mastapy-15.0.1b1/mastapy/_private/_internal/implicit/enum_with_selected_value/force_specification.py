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
from mastapy._private.system_model.analyses_and_results.static_loads import _7809

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self", bound="EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification",)


class EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification

    A specific implementation of 'EnumWithSelectedValue' for 'PointLoadLoadCase.ForceSpecification' types.
    """

    __qualname__ = "PointLoadLoadCase.ForceSpecification"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification]",
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
        cls: "Type[EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification]",
    ) -> "_7809.PointLoadLoadCase.ForceSpecification":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7809.PointLoadLoadCase.ForceSpecification
        """
        return _7809.PointLoadLoadCase.ForceSpecification

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_PointLoadLoadCase_ForceSpecification]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7809.PointLoadLoadCase.ForceSpecification.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_7809.PointLoadLoadCase.ForceSpecification":
        """mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase.ForceSpecification

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_7809.PointLoadLoadCase.ForceSpecification]":
        """List[mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase.ForceSpecification]

        Note:
            This property is readonly.
        """
        return None
