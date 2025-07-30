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
from mastapy._private.nodal_analysis.fe_export_utility import _247

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_FESubstructuringFileFormat")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_FESubstructuringFileFormat",)


class EnumWithSelectedValue_FESubstructuringFileFormat(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_FESubstructuringFileFormat

    A specific implementation of 'EnumWithSelectedValue' for 'FESubstructuringFileFormat' types.
    """

    __qualname__ = "FESubstructuringFileFormat"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_FESubstructuringFileFormat]",
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
        cls: "Type[EnumWithSelectedValue_FESubstructuringFileFormat]",
    ) -> "_247.FESubstructuringFileFormat":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _247.FESubstructuringFileFormat
        """
        return _247.FESubstructuringFileFormat

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_FESubstructuringFileFormat]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _247.FESubstructuringFileFormat.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_247.FESubstructuringFileFormat":
        """mastapy.nodal_analysis.fe_export_utility.FESubstructuringFileFormat

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_247.FESubstructuringFileFormat]":
        """List[mastapy.nodal_analysis.fe_export_utility.FESubstructuringFileFormat]

        Note:
            This property is readonly.
        """
        return None
