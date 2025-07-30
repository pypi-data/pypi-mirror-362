"""Implementations of 'ListWithSelectedItem' in Python.

As Python does not have an implicit operator, this is the next
best solution for implementing these types properly.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from mastapy._private._internal import constructor, conversion, mixins
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._internal.tuple_with_name import TupleWithName

_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="ListWithSelectedItem_TupleWithName")


__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_TupleWithName",)


class ListWithSelectedItem_TupleWithName(
    TupleWithName, mixins.ListWithSelectedItemMixin
):
    """ListWithSelectedItem_TupleWithName

    A specific implementation of 'ListWithSelectedItem' for 'TupleWithName' types.
    """

    __qualname__ = "TupleWithName"

    def __init__(self: "Self", instance_to_wrap: "Any") -> None:
        super().__init__(instance_to_wrap.SelectedValue)
        object.__setattr__(self, "enclosing", instance_to_wrap)

    @classmethod
    def wrapper_type(cls: "Type[ListWithSelectedItem_TupleWithName]") -> "Any":
        """Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return _LIST_WITH_SELECTED_ITEM

    @classmethod
    def implicit_type(cls: "Type[ListWithSelectedItem_TupleWithName]") -> "Any":
        """Implicit Pythonnet type of this class.

        Note:
            This property is readonly.

        Returns:
            Any
        """
        return TupleWithName.TYPE

    @property
    @exception_bridge
    def selected_value(self: "Self") -> "TupleWithName":
        """TupleWithName

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "SelectedValue")

        if temp is None:
            return None

        value = conversion.pn_to_mp_tuple_with_name(temp, (None))

        if value is None:
            return None

        return constructor.new_from_mastapy_class(TupleWithName)(value)

    @property
    @exception_bridge
    def available_values(self: "Self") -> "TupleWithName":
        """TupleWithName

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AvailableValues")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return constructor.new_from_mastapy_class(TupleWithName)(value)

    @property
    @exception_bridge
    def invalid_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "InvalidProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def read_only_properties(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "ReadOnlyProperties")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_properties_are_read_only(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AllPropertiesAreReadOnly")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def all_properties_are_invalid(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.enclosing, "AllPropertiesAreInvalid")

        if temp is None:
            return False

        return temp
