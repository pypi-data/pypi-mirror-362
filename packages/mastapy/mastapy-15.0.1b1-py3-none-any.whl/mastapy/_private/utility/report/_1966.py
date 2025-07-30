"""CustomReportNameableItem"""

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
from mastapy._private.utility.report import _1958

_CUSTOM_REPORT_NAMEABLE_ITEM = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportNameableItem"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results import _2152, _2153, _2156, _2164
    from mastapy._private.gears.gear_designs.cylindrical import _1145
    from mastapy._private.shafts import _20
    from mastapy._private.system_model.analyses_and_results.modal_analyses.reporting import (
        _4990,
        _4994,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4653,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3092,
    )
    from mastapy._private.utility.report import (
        _1937,
        _1945,
        _1946,
        _1947,
        _1948,
        _1950,
        _1951,
        _1955,
        _1957,
        _1964,
        _1965,
        _1967,
        _1969,
        _1972,
        _1974,
        _1975,
        _1977,
    )
    from mastapy._private.utility_gui.charts import _2057, _2058

    Self = TypeVar("Self", bound="CustomReportNameableItem")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportNameableItem._Cast_CustomReportNameableItem"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportNameableItem",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportNameableItem:
    """Special nested class for casting CustomReportNameableItem to subclasses."""

    __parent__: "CustomReportNameableItem"

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
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
    def ad_hoc_custom_table(self: "CastSelf") -> "_1937.AdHocCustomTable":
        from mastapy._private.utility.report import _1937

        return self.__parent__._cast(_1937.AdHocCustomTable)

    @property
    def custom_chart(self: "CastSelf") -> "_1945.CustomChart":
        from mastapy._private.utility.report import _1945

        return self.__parent__._cast(_1945.CustomChart)

    @property
    def custom_drawing(self: "CastSelf") -> "_1946.CustomDrawing":
        from mastapy._private.utility.report import _1946

        return self.__parent__._cast(_1946.CustomDrawing)

    @property
    def custom_graphic(self: "CastSelf") -> "_1947.CustomGraphic":
        from mastapy._private.utility.report import _1947

        return self.__parent__._cast(_1947.CustomGraphic)

    @property
    def custom_image(self: "CastSelf") -> "_1948.CustomImage":
        from mastapy._private.utility.report import _1948

        return self.__parent__._cast(_1948.CustomImage)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "_1950.CustomReportCadDrawing":
        from mastapy._private.utility.report import _1950

        return self.__parent__._cast(_1950.CustomReportCadDrawing)

    @property
    def custom_report_chart(self: "CastSelf") -> "_1951.CustomReportChart":
        from mastapy._private.utility.report import _1951

        return self.__parent__._cast(_1951.CustomReportChart)

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        from mastapy._private.utility.report import _1955

        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

    @property
    def custom_report_html_item(self: "CastSelf") -> "_1957.CustomReportHtmlItem":
        from mastapy._private.utility.report import _1957

        return self.__parent__._cast(_1957.CustomReportHtmlItem)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        from mastapy._private.utility.report import _1964

        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1965.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1965

        return self.__parent__._cast(_1965.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_named_item(self: "CastSelf") -> "_1967.CustomReportNamedItem":
        from mastapy._private.utility.report import _1967

        return self.__parent__._cast(_1967.CustomReportNamedItem)

    @property
    def custom_report_status_item(self: "CastSelf") -> "_1969.CustomReportStatusItem":
        from mastapy._private.utility.report import _1969

        return self.__parent__._cast(_1969.CustomReportStatusItem)

    @property
    def custom_report_text(self: "CastSelf") -> "_1972.CustomReportText":
        from mastapy._private.utility.report import _1972

        return self.__parent__._cast(_1972.CustomReportText)

    @property
    def custom_sub_report(self: "CastSelf") -> "_1974.CustomSubReport":
        from mastapy._private.utility.report import _1974

        return self.__parent__._cast(_1974.CustomSubReport)

    @property
    def custom_table(self: "CastSelf") -> "_1975.CustomTable":
        from mastapy._private.utility.report import _1975

        return self.__parent__._cast(_1975.CustomTable)

    @property
    def dynamic_custom_report_item(self: "CastSelf") -> "_1977.DynamicCustomReportItem":
        from mastapy._private.utility.report import _1977

        return self.__parent__._cast(_1977.DynamicCustomReportItem)

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
    def loaded_bearing_chart_reporter(
        self: "CastSelf",
    ) -> "_2153.LoadedBearingChartReporter":
        from mastapy._private.bearings.bearing_results import _2153

        return self.__parent__._cast(_2153.LoadedBearingChartReporter)

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
    def parametric_study_histogram(
        self: "CastSelf",
    ) -> "_4653.ParametricStudyHistogram":
        from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
            _4653,
        )

        return self.__parent__._cast(_4653.ParametricStudyHistogram)

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
    def custom_report_nameable_item(self: "CastSelf") -> "CustomReportNameableItem":
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
class CustomReportNameableItem(_1958.CustomReportItem):
    """CustomReportNameableItem

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_NAMEABLE_ITEM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def x_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @x_position_for_cad.setter
    @exception_bridge
    @enforce_parameter_types
    def x_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def y_position_for_cad(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YPositionForCAD")

        if temp is None:
            return 0.0

        return temp

    @y_position_for_cad.setter
    @exception_bridge
    @enforce_parameter_types
    def y_position_for_cad(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YPositionForCAD", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportNameableItem":
        """Cast to another type.

        Returns:
            _Cast_CustomReportNameableItem
        """
        return _Cast_CustomReportNameableItem(self)
