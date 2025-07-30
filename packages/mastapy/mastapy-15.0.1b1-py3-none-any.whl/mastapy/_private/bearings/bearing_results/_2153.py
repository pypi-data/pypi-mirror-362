"""LoadedBearingChartReporter"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1948

_LOADED_BEARING_CHART_REPORTER = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBearingChartReporter"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1947, _1955, _1958, _1966

    Self = TypeVar("Self", bound="LoadedBearingChartReporter")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBearingChartReporter._Cast_LoadedBearingChartReporter"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBearingChartReporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBearingChartReporter:
    """Special nested class for casting LoadedBearingChartReporter to subclasses."""

    __parent__: "LoadedBearingChartReporter"

    @property
    def custom_image(self: "CastSelf") -> "_1948.CustomImage":
        return self.__parent__._cast(_1948.CustomImage)

    @property
    def custom_graphic(self: "CastSelf") -> "_1947.CustomGraphic":
        from mastapy._private.utility.report import _1947

        return self.__parent__._cast(_1947.CustomGraphic)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1955

        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def loaded_bearing_chart_reporter(self: "CastSelf") -> "LoadedBearingChartReporter":
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
class LoadedBearingChartReporter(_1948.CustomImage):
    """LoadedBearingChartReporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BEARING_CHART_REPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def property_(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(self.wrapped, "Property")

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @property_.setter
    @exception_bridge
    @enforce_parameter_types
    def property_(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "Property", value)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBearingChartReporter":
        """Cast to another type.

        Returns:
            _Cast_LoadedBearingChartReporter
        """
        return _Cast_LoadedBearingChartReporter(self)
