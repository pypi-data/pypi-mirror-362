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
from mastapy._private.system_model.part_model import _2707

_ARRAY = python_net_import("System", "Array")
_ENUM_WITH_SELECTED_VALUE = python_net_import(
    "SMT.MastaAPI.Utility.Property", "EnumWithSelectedValue"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing",)


class EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing(
    mixins.EnumWithSelectedValueMixin, Enum
):
    """EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing

    A specific implementation of 'EnumWithSelectedValue' for 'ShaftDiameterModificationDueToRollingBearingRing' types.
    """

    __qualname__ = "ShaftDiameterModificationDueToRollingBearingRing"

    @classmethod
    def wrapper_type(
        cls: "Type[EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing]",
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
        cls: "Type[EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing]",
    ) -> "_2707.ShaftDiameterModificationDueToRollingBearingRing":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _2707.ShaftDiameterModificationDueToRollingBearingRing
        """
        return _2707.ShaftDiameterModificationDueToRollingBearingRing

    @classmethod
    def implicit_type(
        cls: "Type[EnumWithSelectedValue_ShaftDiameterModificationDueToRollingBearingRing]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _2707.ShaftDiameterModificationDueToRollingBearingRing.type_()

    @property
    @exception_bridge
    def selected_value(
        self: "Self",
    ) -> "_2707.ShaftDiameterModificationDueToRollingBearingRing":
        """mastapy.system_model.part_model.ShaftDiameterModificationDueToRollingBearingRing

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(
        self: "Self",
    ) -> "List[_2707.ShaftDiameterModificationDueToRollingBearingRing]":
        """List[mastapy.system_model.part_model.ShaftDiameterModificationDueToRollingBearingRing]

        Note:
            This property is readonly.
        """
        return None
