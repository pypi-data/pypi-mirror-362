"""Customer102DataSheetChangeLogItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CUSTOMER_102_DATA_SHEET_CHANGE_LOG_ITEM = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "Customer102DataSheetChangeLogItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Customer102DataSheetChangeLogItem")
    CastSelf = TypeVar(
        "CastSelf",
        bound="Customer102DataSheetChangeLogItem._Cast_Customer102DataSheetChangeLogItem",
    )


__docformat__ = "restructuredtext en"
__all__ = ("Customer102DataSheetChangeLogItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Customer102DataSheetChangeLogItem:
    """Special nested class for casting Customer102DataSheetChangeLogItem to subclasses."""

    __parent__: "Customer102DataSheetChangeLogItem"

    @property
    def customer_102_data_sheet_change_log_item(
        self: "CastSelf",
    ) -> "Customer102DataSheetChangeLogItem":
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
class Customer102DataSheetChangeLogItem(_0.APIBase):
    """Customer102DataSheetChangeLogItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOMER_102_DATA_SHEET_CHANGE_LOG_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def change(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Change")

        if temp is None:
            return ""

        return temp

    @change.setter
    @exception_bridge
    @enforce_parameter_types
    def change(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Change", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def engineer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Engineer")

        if temp is None:
            return ""

        return temp

    @engineer.setter
    @exception_bridge
    @enforce_parameter_types
    def engineer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Engineer", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def rev(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Rev")

        if temp is None:
            return ""

        return temp

    @rev.setter
    @exception_bridge
    @enforce_parameter_types
    def rev(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Rev", str(value) if value is not None else ""
        )

    @exception_bridge
    def remove_revision(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveRevision")

    @property
    def cast_to(self: "Self") -> "_Cast_Customer102DataSheetChangeLogItem":
        """Cast to another type.

        Returns:
            _Cast_Customer102DataSheetChangeLogItem
        """
        return _Cast_Customer102DataSheetChangeLogItem(self)
