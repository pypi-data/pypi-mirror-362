"""Implementations of 'ListWithSelectedItem' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal import mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import python_net_import
from mastapy._private._internal.tuple_with_name import TupleWithName
from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1225

_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ListWithSelectedItem_DrawDefiningGearOrBoth")


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_DrawDefiningGearOrBoth",)


class ListWithSelectedItem_DrawDefiningGearOrBoth(
    mixins.ListWithSelectedItemMixin, Enum
):
    """ListWithSelectedItem_DrawDefiningGearOrBoth

    A specific implementation of 'ListWithSelectedItem' for 'DrawDefiningGearOrBoth' types.
    """

    __qualname__ = "DrawDefiningGearOrBoth"

    @classmethod
    def wrapper_type(cls: "Type[ListWithSelectedItem_DrawDefiningGearOrBoth]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def wrapped_type(
        cls: "Type[ListWithSelectedItem_DrawDefiningGearOrBoth]",
    ) -> "_1225.DrawDefiningGearOrBoth":
        """Wrapped Pythonnet type of this class.

        Note:
            This property is readonly

        Returns:
            _1225.DrawDefiningGearOrBoth
        """
        return _1225.DrawDefiningGearOrBoth

    @classmethod
    def implicit_type(
        cls: "Type[ListWithSelectedItem_DrawDefiningGearOrBoth]",
    ) -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _1225.DrawDefiningGearOrBoth.type_()

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "TupleWithName":
        """TupleWithName

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def available_values(self: "Self") -> "TupleWithName":
        """TupleWithName

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def invalid_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def read_only_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def all_properties_are_read_only(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None

    @property
    @exception_bridge
    def all_properties_are_invalid(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        return None
