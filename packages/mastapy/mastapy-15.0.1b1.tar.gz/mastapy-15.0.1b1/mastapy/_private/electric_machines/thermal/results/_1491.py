"""ThermalResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_RESULTS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal.Results", "ThermalResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses import (
        _1497,
        _1498,
        _1499,
        _1501,
    )
    from mastapy._private.electric_machines.thermal.results import _1492, _1495

    Self = TypeVar("Self", bound="ThermalResults")
    CastSelf = TypeVar("CastSelf", bound="ThermalResults._Cast_ThermalResults")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalResults:
    """Special nested class for casting ThermalResults to subclasses."""

    __parent__: "ThermalResults"

    @property
    def thermal_results(self: "CastSelf") -> "ThermalResults":
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
class ThermalResults(_0.APIBase):
    """ThermalResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def fe_thermal_results(self: "Self") -> "List[_1492.ThermalResultsForFEComponent]":
        """List[mastapy.electric_machines.thermal.results.ThermalResultsForFEComponent]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEThermalResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def heat_dissipation(self: "Self") -> "List[_1497.HeatDissipationReporter]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.HeatDissipationReporter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatDissipation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def heat_flows(self: "Self") -> "List[_1498.HeatFlowReporter]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.HeatFlowReporter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatFlows")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def heat_transfer_coefficients(
        self: "Self",
    ) -> "List[_1499.HeatTransferCoefficientReporter]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.HeatTransferCoefficientReporter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatTransferCoefficients")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def lptn_node_results(self: "Self") -> "List[_1495.ThermalResultsForLPTNNode]":
        """List[mastapy.electric_machines.thermal.results.ThermalResultsForLPTNNode]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LPTNNodeResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def pressure_drops(self: "Self") -> "List[_1501.PressureDropReporter]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.PressureDropReporter]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureDrops")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_ThermalResults":
        """Cast to another type.

        Returns:
            _Cast_ThermalResults
        """
        return _Cast_ThermalResults(self)
