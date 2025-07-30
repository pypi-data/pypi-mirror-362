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
from mastapy._private.bearings.tolerances import _2113

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_ITDesignation")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ITDesignation",)


class EnumWithSelectedValue_ITDesignation(mixins.EnumWithSelectedValueMixin, Enum):
    """EnumWithSelectedValue_ITDesignation

    A specific implementation of 'EnumWithSelectedValue' for 'ITDesignation' types.
    """

    __qualname__ = "ITDesignation"

    @classmethod
    def wrapper_type(cls: "Type[EnumWithSelectedValue_ITDesignation]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _ENUM_WITH_SELECTED_VALUE

    @classmethod
    def wrapped_type(
        cls: "Type[EnumWithSelectedValue_ITDesignation]",
    ) -> "_2113.ITDesignation":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2113.ITDesignation
        """
        return _2113.ITDesignation

    @classmethod
    def implicit_type(cls: "Type[EnumWithSelectedValue_ITDesignation]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2113.ITDesignation.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_2113.ITDesignation":
        """mastapy.bearings.tolerances.ITDesignation

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_2113.ITDesignation]":
        """List[mastapy.bearings.tolerances.ITDesignation]

        Note:
            This property is readonly.
        """
        return None
