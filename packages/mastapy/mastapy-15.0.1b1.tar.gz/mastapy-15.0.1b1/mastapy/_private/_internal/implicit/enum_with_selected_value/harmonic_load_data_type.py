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
from mastapy._private.electric_machines.harmonic_load_data import _1566

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_HarmonicLoadDataType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_HarmonicLoadDataType",)


class EnumWithSelectedValue_HarmonicLoadDataType(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_HarmonicLoadDataType

    A specific implementation of 'EnumWithSelectedValue' for 'HarmonicLoadDataType' types.
    """

    __qualname__ = "HarmonicLoadDataType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_HarmonicLoadDataType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_HarmonicLoadDataType]",
    ) -> "_1566.HarmonicLoadDataType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1566.HarmonicLoadDataType
        """
        return _1566.HarmonicLoadDataType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_HarmonicLoadDataType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1566.HarmonicLoadDataType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1566.HarmonicLoadDataType":
        """mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1566.HarmonicLoadDataType]":
        """List[mastapy.electric_machines.harmonic_load_data.HarmonicLoadDataType]

        Note:
            This property is readonly.
        """
        return None
