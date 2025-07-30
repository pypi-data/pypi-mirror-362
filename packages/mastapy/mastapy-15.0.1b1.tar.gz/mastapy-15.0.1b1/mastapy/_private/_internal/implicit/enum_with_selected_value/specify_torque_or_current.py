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
from mastapy._private.electric_machines.load_cases_and_analyses import _1556

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_SpecifyTorqueOrCurrent")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_SpecifyTorqueOrCurrent",)


class EnumWithSelectedValue_SpecifyTorqueOrCurrent(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_SpecifyTorqueOrCurrent

    A specific implementation of 'EnumWithSelectedValue' for 'SpecifyTorqueOrCurrent' types.
    """

    __qualname__ = "SpecifyTorqueOrCurrent"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_SpecifyTorqueOrCurrent]",
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
        cls: "Type[EnumWithSelectedValue_SpecifyTorqueOrCurrent]",
    ) -> "_1556.SpecifyTorqueOrCurrent":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1556.SpecifyTorqueOrCurrent
        """
        return _1556.SpecifyTorqueOrCurrent

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_SpecifyTorqueOrCurrent]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1556.SpecifyTorqueOrCurrent.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1556.SpecifyTorqueOrCurrent":
        """mastapy.electric_machines.load_cases_and_analyses.SpecifyTorqueOrCurrent

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1556.SpecifyTorqueOrCurrent]":
        """List[mastapy.electric_machines.load_cases_and_analyses.SpecifyTorqueOrCurrent]

        Note:
            This property is readonly.
        """
        return None
