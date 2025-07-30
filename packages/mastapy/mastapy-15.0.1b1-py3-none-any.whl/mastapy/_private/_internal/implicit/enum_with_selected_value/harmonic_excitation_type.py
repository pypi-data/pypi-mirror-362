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
from mastapy._private.system_model.analyses_and_results.static_loads import _7766

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_HarmonicExcitationType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_HarmonicExcitationType",)


class EnumWithSelectedValue_HarmonicExcitationType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_HarmonicExcitationType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicExcitationType' types.
    """

    __qualname__ = "HarmonicExcitationType"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_HarmonicExcitationType]",
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
        cls: "Type[EnumWithSelectedValue_HarmonicExcitationType]",
    ) -> "_7766.HarmonicExcitationType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7766.HarmonicExcitationType
        """
        return _7766.HarmonicExcitationType

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_HarmonicExcitationType]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7766.HarmonicExcitationType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_7766.HarmonicExcitationType":
        """mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_7766.HarmonicExcitationType]":
        """List[mastapy.system_model.analyses_and_results.static_loads.HarmonicExcitationType]

        Note:
            This property is readonly.
        """
        return None
