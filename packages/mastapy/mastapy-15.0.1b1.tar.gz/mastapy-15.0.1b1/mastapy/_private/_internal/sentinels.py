"""Sentinel classes representing None values for implicit types."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, ClassVar, List, Type, TypeVar

    from mastapy._0 import APIBase

    Self = TypeVar("Self", bound="ListWithSelectedItem_None")

from mastapy._private._internal import conversion, mixins
from mastapy._private._internal.python_net import python_net_import

_LIST_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Property", "ListWithSelectedItem"
)

__docformat__ = "restructuredtext en"
__all__ = ("ListWithSelectedItem_None",)


@dataclass(frozen=True)
class ListWithSelectedItem_None(mixins.ListWithSelectedItemMixin):
    """Sentinel class for list with selected items. Equivalent to None."""

    enclosing: "Any"
    __qualname__: "ClassVar[str]" = "None"

    @classmethod
    def wrapper_type(
        cls: "Type[ListWithSelectedItem_None]",
    ) -> "Any":
        """Pythonnet type of this class."""
        return _LIST_WITH_SELECTED_ITEM

    @property
    def selected_value(self: "Self") -> None:
        """Selected value of list. Always returns None for sentinels.

        Returns:
            None
        """
        return None

    @property
    def available_values(self: "Self") -> "List[APIBase]":
        """Available values in the list.

        Returns:
            List[Any]
        """
        temp = self.enclosing.AvailableValues

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    def __eq__(self: "Self", other: object) -> bool:
        """Override of the equals magic method.

        This is a hack to ensure self == None checks return True.

        Args:
            other (object): Other object.

        Returns:
            bool
        """
        return other is None

    def __bool__(self: "Self") -> bool:
        """Override of the bool magic method.

        Returns:
            bool
        """
        return False
