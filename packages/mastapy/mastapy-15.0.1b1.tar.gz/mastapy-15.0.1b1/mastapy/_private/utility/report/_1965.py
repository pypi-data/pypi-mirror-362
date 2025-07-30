"""CustomReportMultiPropertyItemBase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.utility.report import _1966

_CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportMultiPropertyItemBase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2152, _2156, _2164
    from mastapy._private.gears.gear_designs.cylindrical import _1145
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4990,
        _4994,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3092,
    )
    from mastapy._private.utility.report import _1951, _1958, _1964, _1975
    from mastapy._private.utility_gui.charts import _2057, _2058

    Self = TypeVar("Self", bound="CustomReportMultiPropertyItemBase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CustomReportMultiPropertyItemBase._Cast_CustomReportMultiPropertyItemBase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportMultiPropertyItemBase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportMultiPropertyItemBase:
    """Special nested class for casting CustomReportMultiPropertyItemBase to subclasses."""

    __parent__: "CustomReportMultiPropertyItemBase"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
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
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "_1145.CylindricalGearTableWithMGCharts":
        from mastapy._private.gears.gear_designs.cylindrical import _1145

        return self.__parent__._cast(_1145.CylindricalGearTableWithMGCharts)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1951.CustomReportChart":
        from mastapy._private.utility.report import _1951

        return self.__parent__._cast(_1951.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1964

        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_table(self: "CastSelf") -> "_1975.CustomTable":
        from mastapy._private.utility.report import _1975

        return self.__parent__._cast(_1975.CustomTable)

    @property
    def custom_line_chart(self: "CastSelf") -> "_2057.CustomLineChart":
        from mastapy._private.utility_gui.charts import _2057

        return self.__parent__._cast(_2057.CustomLineChart)

    @property
    def custom_table_and_chart(self: "CastSelf") -> "_2058.CustomTableAndChart":
        from mastapy._private.utility_gui.charts import _2058

        return self.__parent__._cast(_2058.CustomTableAndChart)

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
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "CustomReportMultiPropertyItemBase":
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
class CustomReportMultiPropertyItemBase(_1966.CustomReportNameableItem):
    """CustomReportMultiPropertyItemBase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_MULTI_PROPERTY_ITEM_BASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportMultiPropertyItemBase":
        """Cast to another type.

        Returns:
            _Cast_CustomReportMultiPropertyItemBase
        """
        return _Cast_CustomReportMultiPropertyItemBase(self)
