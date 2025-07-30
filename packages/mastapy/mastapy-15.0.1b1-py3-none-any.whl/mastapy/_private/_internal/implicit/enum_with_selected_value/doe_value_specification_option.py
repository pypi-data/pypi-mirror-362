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
from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
    _4614,
)

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DoeValueSpecificationOption")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DoeValueSpecificationOption",)


class EnumWithSelectedValue_DoeValueSpecificationOption(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DoeValueSpecificationOption

    A specific implementation of 'EnumWithSelectedValue' for 'DoeValueSpecificationOption' types.
    """

    __qualname__ = "DoeValueSpecificationOption"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_DoeValueSpecificationOption]",
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
        cls: "Type[EnumWithSelectedValue_DoeValueSpecificationOption]",
    ) -> "_4614.DoeValueSpecificationOption":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _4614.DoeValueSpecificationOption
        """
        return _4614.DoeValueSpecificationOption

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_DoeValueSpecificationOption]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _4614.DoeValueSpecificationOption.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_4614.DoeValueSpecificationOption":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DoeValueSpecificationOption

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_4614.DoeValueSpecificationOption]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.DoeValueSpecificationOption]

        Note:
            This property is readonly.
        """
        return None
