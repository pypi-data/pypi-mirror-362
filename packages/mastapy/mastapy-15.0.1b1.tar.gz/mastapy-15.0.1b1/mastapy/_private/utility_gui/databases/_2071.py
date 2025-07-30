"""DatabaseWithSelectedItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    Self = TypeVar("Self", bound="DatabaseWithSelectedItem")
    CastSelf = TypeVar(
        "CastSelf", bound="DatabaseWithSelectedItem._Cast_DatabaseWithSelectedItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DatabaseWithSelectedItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DatabaseWithSelectedItem:
    """Special nested class for casting DatabaseWithSelectedItem to subclasses."""

    __parent__: "DatabaseWithSelectedItem"

    @property
    def database_with_selected_item(self: "CastSelf") -> "DatabaseWithSelectedItem":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class DatabaseWithSelectedItem(_0.APIBase):
    """DatabaseWithSelectedItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DATABASE_WITH_SELECTED_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def items(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Items")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def selected_item_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SelectedItemName")

        if temp is None:
            return ""

        return temp

    @exception_bridge
    @enforce_parameter_types
    def set_selected_item(self: "Self", item_name: "str") -> None:
        """Method does not return.

        Args:
            item_name (str)
        """
        item_name = str(item_name)
        pythonnet_method_call(
            self.wrapped, "SetSelectedItem", item_name if item_name else ""
        )

    @property
    def cast_to(self: "Self") -> "_Cast_DatabaseWithSelectedItem":
        """Cast to another type.

        Returns:
            _Cast_DatabaseWithSelectedItem
        """
        return _Cast_DatabaseWithSelectedItem(self)
