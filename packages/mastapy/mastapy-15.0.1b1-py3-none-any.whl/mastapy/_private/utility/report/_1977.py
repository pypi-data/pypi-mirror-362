"""DynamicCustomReportItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1966

_DYNAMIC_CUSTOM_REPORT_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "DynamicCustomReportItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958

    Self = TypeVar("Self", bound="DynamicCustomReportItem")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicCustomReportItem._Cast_DynamicCustomReportItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicCustomReportItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DynamicCustomReportItem:
    """Special nested class for casting DynamicCustomReportItem to subclasses."""

    __parent__: "DynamicCustomReportItem"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "DynamicCustomReportItem":
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
class DynamicCustomReportItem(_1966.CustomReportNameableItem):
    """DynamicCustomReportItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DYNAMIC_CUSTOM_REPORT_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def is_main_report_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsMainReportItem")

        if temp is None:
            return False

        return temp

    @is_main_report_item.setter
    @exception_bridge
    @enforce_parameter_types
    def is_main_report_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IsMainReportItem",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def inner_item(self: "Self") -> "_1958.CustomReportItem":
        """mastapy.utility.report.CustomReportItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerItem")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_DynamicCustomReportItem":
        """Cast to another type.

        Returns:
            _Cast_DynamicCustomReportItem
        """
        return _Cast_DynamicCustomReportItem(self)
