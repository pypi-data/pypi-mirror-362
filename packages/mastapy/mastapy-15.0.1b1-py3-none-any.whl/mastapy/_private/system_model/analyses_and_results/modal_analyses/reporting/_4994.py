"""PerModeResultsReport"""

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
from mastapy._private.utility.report import _1951

_PER_MODE_RESULTS_REPORT = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses.Reporting",
    "PerModeResultsReport",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.enums import _2018
    from mastapy._private.utility.report import _1958, _1964, _1965, _1966

    Self = TypeVar("Self", bound="PerModeResultsReport")
    CastSelf = TypeVar(
        "CastSelf", bound="PerModeResultsReport._Cast_PerModeResultsReport"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PerModeResultsReport",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PerModeResultsReport:
    """Special nested class for casting PerModeResultsReport to subclasses."""

    __parent__: "PerModeResultsReport"

    @property
    def custom_report_chart(self: "CastSelf") -> "_1951.CustomReportChart":
        return self.__parent__._cast(_1951.CustomReportChart)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1964

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
    def per_mode_results_report(self: "CastSelf") -> "PerModeResultsReport":
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
class PerModeResultsReport(_1951.CustomReportChart):
    """PerModeResultsReport

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PER_MODE_RESULTS_REPORT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def display_option(self: "Self") -> "_2018.TableAndChartOptions":
        """mastapy.utility.enums.TableAndChartOptions"""
        temp = pythonnet_property_get(self.wrapped, "DisplayOption")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.enums._2018", "TableAndChartOptions"
        )(value)

    @display_option.setter
    @exception_bridge
    @enforce_parameter_types
    def display_option(self: "Self", value: "_2018.TableAndChartOptions") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.Enums.TableAndChartOptions"
        )
        pythonnet_property_set(self.wrapped, "DisplayOption", value)

    @property
    @exception_bridge
    def include_connected_parts_for_connections(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "IncludeConnectedPartsForConnections"
        )

        if temp is None:
            return False

        return temp

    @include_connected_parts_for_connections.setter
    @exception_bridge
    @enforce_parameter_types
    def include_connected_parts_for_connections(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeConnectedPartsForConnections",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_number_of_modes_to_show_on_a_single_table_or_chart(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNumberOfModesToShowOnASingleTableOrChart"
        )

        if temp is None:
            return 0

        return temp

    @maximum_number_of_modes_to_show_on_a_single_table_or_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_modes_to_show_on_a_single_table_or_chart(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfModesToShowOnASingleTableOrChart",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def show_all_modes(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ShowAllModes")

        if temp is None:
            return False

        return temp

    @show_all_modes.setter
    @exception_bridge
    @enforce_parameter_types
    def show_all_modes(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ShowAllModes", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def transpose_chart(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TransposeChart")

        if temp is None:
            return False

        return temp

    @transpose_chart.setter
    @exception_bridge
    @enforce_parameter_types
    def transpose_chart(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "TransposeChart", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def transpose_table(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "TransposeTable")

        if temp is None:
            return False

        return temp

    @transpose_table.setter
    @exception_bridge
    @enforce_parameter_types
    def transpose_table(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "TransposeTable", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PerModeResultsReport":
        """Cast to another type.

        Returns:
            _Cast_PerModeResultsReport
        """
        return _Cast_PerModeResultsReport(self)
