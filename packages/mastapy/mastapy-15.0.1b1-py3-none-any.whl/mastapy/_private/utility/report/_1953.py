"""CustomReportColumn"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1962

_CUSTOM_REPORT_COLUMN = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportColumn"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1959

    Self = TypeVar("Self", bound="CustomReportColumn")
    CastSelf = TypeVar("CastSelf", bound="CustomReportColumn._Cast_CustomReportColumn")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportColumn",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportColumn:
    """Special nested class for casting CustomReportColumn to subclasses."""

    __parent__: "CustomReportColumn"

    @property
    def custom_report_item_container_collection_item(
        self: "CastSelf",
    ) -> "_1962.CustomReportItemContainerCollectionItem":
        return self.__parent__._cast(_1962.CustomReportItemContainerCollectionItem)

    @property
    def custom_report_item_container(
        self: "CastSelf",
    ) -> "_1959.CustomReportItemContainer":
        from mastapy._private.utility.report import _1959

        return self.__parent__._cast(_1959.CustomReportItemContainer)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_column(self: "CastSelf") -> "CustomReportColumn":
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
class CustomReportColumn(_1962.CustomReportItemContainerCollectionItem):
    """CustomReportColumn

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_COLUMN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auto_width(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "AutoWidth")

        if temp is None:
            return False

        return temp

    @auto_width.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_width(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "AutoWidth", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportColumn":
        """Cast to another type.

        Returns:
            _Cast_CustomReportColumn
        """
        return _Cast_CustomReportColumn(self)
