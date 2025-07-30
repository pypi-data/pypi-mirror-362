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
from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
    _7863,
)

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="EnumWithSelectedValue_DestinationDesignState")


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_DestinationDesignState",)


class EnumWithSelectedValue_DestinationDesignState(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_DestinationDesignState

    A specific implementation of 'EnumWithSelectedValue' for 'DestinationDesignState' types.
    """

    __qualname__ = "DestinationDesignState"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_DestinationDesignState]",
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
        cls: "Type[EnumWithSelectedValue_DestinationDesignState]",
    ) -> "_7863.DestinationDesignState":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _7863.DestinationDesignState
        """
        return _7863.DestinationDesignState

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_DestinationDesignState]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _7863.DestinationDesignState.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "_7863.DestinationDesignState":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.DestinationDesignState

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "List[_7863.DestinationDesignState]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.DestinationDesignState]

        Note:
            This property is readonly.
        """
        return None
