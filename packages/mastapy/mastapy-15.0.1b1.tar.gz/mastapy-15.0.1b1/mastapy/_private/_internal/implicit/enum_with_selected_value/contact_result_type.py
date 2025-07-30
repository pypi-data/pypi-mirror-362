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
from mastapy._private.gears.ltca import _930

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ContactResultType")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ContactResultType",)


class EnumWithSelectedValue_ContactResultType(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ContactResultType

    A specific implementation of 'EnumWithSelectedValue' for 'ContactResultType' types.
    """

    __qualname__ = "ContactResultType"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ContactResultType]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ContactResultType]",
    ) -> "_930.ContactResultType":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _930.ContactResultType
        """
        return _930.ContactResultType

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ContactResultType]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _930.ContactResultType.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_930.ContactResultType":
        """mastapy.gears.ltca.ContactResultType

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_930.ContactResultType]":
        """List[mastapy.gears.ltca.ContactResultType]

        Note:
            This property is readonly.
        """
        return None
