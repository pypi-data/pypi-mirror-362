"""CustomReportChartItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1968

_CUSTOM_REPORT_CHART_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportChartItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1944

    Self = TypeVar("Self", bound="CustomReportChartItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportChartItem._Cast_CustomReportChartItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportChartItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportChartItem:
    """Special nested class for casting CustomReportChartItem to subclasses."""

    __parent__: "CustomReportChartItem"

    @property
    def custom_report_property_item(
        self: "CastSelf",
    ) -> "_1968.CustomReportPropertyItem":
        return self.__parent__._cast(_1968.CustomReportPropertyItem)

    @property
    def custom_report_chart_item(self: "CastSelf") -> "CustomReportChartItem":
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
class CustomReportChartItem(_1968.CustomReportPropertyItem):
    """CustomReportChartItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_CHART_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def has_marker(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasMarker")

        if temp is None:
            return False

        return temp

    @has_marker.setter
    @exception_bridge
    @enforce_parameter_types
    def has_marker(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "HasMarker", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def marker_size(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MarkerSize")

        if temp is None:
            return 0.0

        return temp

    @marker_size.setter
    @exception_bridge
    @enforce_parameter_types
    def marker_size(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MarkerSize", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def point_shape(self: "Self") -> "_1944.SMTChartPointShape":
        """mastapy.utility.report.SMTChartPointShape"""
        temp = pythonnet_property_get(self.wrapped, "PointShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Report.SMTChartPointShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1944", "SMTChartPointShape"
        )(value)

    @point_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def point_shape(self: "Self", value: "_1944.SMTChartPointShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.SMTChartPointShape"
        )
        pythonnet_property_set(self.wrapped, "PointShape", value)

    @property
    @exception_bridge
    def smooth_lines(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SmoothLines")

        if temp is None:
            return False

        return temp

    @smooth_lines.setter
    @exception_bridge
    @enforce_parameter_types
    def smooth_lines(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "SmoothLines", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportChartItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportChartItem
        """
        return _Cast_CustomReportChartItem(self)
