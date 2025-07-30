"""CustomReportChart"""

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
from mastapy._private.utility.report import _1952, _1964

_CUSTOM_REPORT_CHART = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportChart"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2152, _2156, _2164
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4990,
        _4994,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3092,
    )
    from mastapy._private.utility.report import _1958, _1965, _1966
    from mastapy._private.utility_gui.charts import _2057

    Self = TypeVar("Self", bound="CustomReportChart")
    CastSelf = TypeVar("CastSelf", bound="CustomReportChart._Cast_CustomReportChart")


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportChart",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportChart:
    """Special nested class for casting CustomReportChart to subclasses."""

    __parent__: "CustomReportChart"

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1965.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1965

        return self.__parent__._cast(_1965.CustomReportMultiPropertyItemBase)

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
    def shaft_damage_results_table_and_chart(
        self: "CastSelf",
    ) -> "_20.ShaftDamageResultsTableAndChart":
        from mastapy._private.shafts import _20

        return self.__parent__._cast(_20.ShaftDamageResultsTableAndChart)

    @property
    def custom_line_chart(self: "CastSelf") -> "_2057.CustomLineChart":
        from mastapy._private.utility_gui.charts import _2057

        return self.__parent__._cast(_2057.CustomLineChart)

    @property
    def loaded_ball_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2152.LoadedBallElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2152

        return self.__parent__._cast(_2152.LoadedBallElementChartReporter)

    @property
    def loaded_bearing_temperature_chart(
        self: "CastSelf",
    ) -> "_2156.LoadedBearingTemperatureChart":
        from mastapy._private.bearings.bearing_results import _2156

        return self.__parent__._cast(_2156.LoadedBearingTemperatureChart)

    @property
    def loaded_roller_element_chart_reporter(
        self: "CastSelf",
    ) -> "_2164.LoadedRollerElementChartReporter":
        from mastapy._private.bearings.bearing_results import _2164

        return self.__parent__._cast(_2164.LoadedRollerElementChartReporter)

    @property
    def shaft_system_deflection_sections_report(
        self: "CastSelf",
    ) -> "_3092.ShaftSystemDeflectionSectionsReport":
        from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
            _3092,
        )

        return self.__parent__._cast(_3092.ShaftSystemDeflectionSectionsReport)

    @property
    def campbell_diagram_report(self: "CastSelf") -> "_4990.CampbellDiagramReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4990,
        )

        return self.__parent__._cast(_4990.CampbellDiagramReport)

    @property
    def per_mode_results_report(self: "CastSelf") -> "_4994.PerModeResultsReport":
        from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
            _4994,
        )

        return self.__parent__._cast(_4994.PerModeResultsReport)

    @property
    def custom_report_chart(self: "CastSelf") -> "CustomReportChart":
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
class CustomReportChart(
    _1964.CustomReportMultiPropertyItem[_1952.CustomReportChartItem]
):
    """CustomReportChart

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_CHART

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def height(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0

        return temp

    @height.setter
    @exception_bridge
    @enforce_parameter_types
    def height(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportChart":
        """Cast to another type.

        Returns:
            _Cast_CustomReportChart
        """
        return _Cast_CustomReportChart(self)
