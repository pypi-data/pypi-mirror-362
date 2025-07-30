"""CustomReportPropertyItem"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
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

_CUSTOM_REPORT_PROPERTY_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportPropertyItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1939, _1952, _1973, _1978, _1979, _1982
    from mastapy._private.utility.reporting_property_framework import _1983

    Self = TypeVar("Self", bound="CustomReportPropertyItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportPropertyItem._Cast_CustomReportPropertyItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportPropertyItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportPropertyItem:
    """Special nested class for casting CustomReportPropertyItem to subclasses."""

    __parent__: "CustomReportPropertyItem"

    @property
    def blank_row(self: "CastSelf") -> "_1939.BlankRow":
        from mastapy._private.utility.report import _1939

        return self.__parent__._cast(_1939.BlankRow)

    @property
    def custom_report_chart_item(self: "CastSelf") -> "_1952.CustomReportChartItem":
        from mastapy._private.utility.report import _1952

        return self.__parent__._cast(_1952.CustomReportChartItem)

    @property
    def custom_row(self: "CastSelf") -> "_1973.CustomRow":
        from mastapy._private.utility.report import _1973

        return self.__parent__._cast(_1973.CustomRow)

    @property
    def user_text_row(self: "CastSelf") -> "_1982.UserTextRow":
        from mastapy._private.utility.report import _1982

        return self.__parent__._cast(_1982.UserTextRow)

    @property
    def custom_report_property_item(self: "CastSelf") -> "CustomReportPropertyItem":
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
class CustomReportPropertyItem(_0.APIBase):
    """CustomReportPropertyItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_PROPERTY_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def font_style(self: "Self") -> "_1978.FontStyle":
        """mastapy.utility.report.FontStyle"""
        temp = pythonnet_property_get(self.wrapped, "FontStyle")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Utility.Report.FontStyle")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1978", "FontStyle"
        )(value)

    @font_style.setter
    @exception_bridge
    @enforce_parameter_types
    def font_style(self: "Self", value: "_1978.FontStyle") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Utility.Report.FontStyle")
        pythonnet_property_set(self.wrapped, "FontStyle", value)

    @property
    @exception_bridge
    def font_weight(self: "Self") -> "_1979.FontWeight":
        """mastapy.utility.report.FontWeight"""
        temp = pythonnet_property_get(self.wrapped, "FontWeight")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Utility.Report.FontWeight")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.report._1979", "FontWeight"
        )(value)

    @font_weight.setter
    @exception_bridge
    @enforce_parameter_types
    def font_weight(self: "Self", value: "_1979.FontWeight") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Report.FontWeight"
        )
        pythonnet_property_set(self.wrapped, "FontWeight", value)

    @property
    @exception_bridge
    def horizontal_position(self: "Self") -> "_1983.CellValuePosition":
        """mastapy.utility.reporting_property_framework.CellValuePosition"""
        temp = pythonnet_property_get(self.wrapped, "HorizontalPosition")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.ReportingPropertyFramework.CellValuePosition"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.reporting_property_framework._1983",
            "CellValuePosition",
        )(value)

    @horizontal_position.setter
    @exception_bridge
    @enforce_parameter_types
    def horizontal_position(self: "Self", value: "_1983.CellValuePosition") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.ReportingPropertyFramework.CellValuePosition"
        )
        pythonnet_property_set(self.wrapped, "HorizontalPosition", value)

    @property
    @exception_bridge
    def show_property_name(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowPropertyName")

        if temp is None:
            return False

        return temp

    @show_property_name.setter
    @exception_bridge
    @enforce_parameter_types
    def show_property_name(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShowPropertyName",
            bool(value) if value is not None else False,
        )

    @exception_bridge
    def add_condition(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "AddCondition")

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportPropertyItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportPropertyItem
        """
        return _Cast_CustomReportPropertyItem(self)
