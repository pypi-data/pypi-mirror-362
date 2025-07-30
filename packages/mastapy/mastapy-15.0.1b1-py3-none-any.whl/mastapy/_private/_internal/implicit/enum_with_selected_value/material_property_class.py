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
from mastapy._private.fe_tools.enums import _1364

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_MaterialPropertyClass")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_MaterialPropertyClass",)


class EnumWithSelectedValue_MaterialPropertyClass(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_MaterialPropertyClass

    A specific implementation of 'EnumWithSelectedValue' for 'MaterialPropertyClass' types.
    """

    __qualname__ = "MaterialPropertyClass"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_MaterialPropertyClass]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_MaterialPropertyClass]",
    ) -> "_1364.MaterialPropertyClass":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1364.MaterialPropertyClass
        """
        return _1364.MaterialPropertyClass

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_MaterialPropertyClass]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1364.MaterialPropertyClass.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_1364.MaterialPropertyClass":
        """mastapy.fe_tools.enums.MaterialPropertyClass

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_1364.MaterialPropertyClass]":
        """List[mastapy.fe_tools.enums.MaterialPropertyClass]

        Note:
            This property is readonly.
        """
        return None
