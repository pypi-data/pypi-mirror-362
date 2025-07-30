"""ThermalAnalysis"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal.LoadCasesAndAnalyses", "ThermalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal import _1480, _1481
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses import _1503
    from mastapy._private.electric_machines.thermal.results import _1491
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _220,
        _226,
    )

    Self = TypeVar("Self", bound="ThermalAnalysis")
    CastSelf = TypeVar("CastSelf", bound="ThermalAnalysis._Cast_ThermalAnalysis")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalAnalysis:
    """Special nested class for casting ThermalAnalysis to subclasses."""

    __parent__: "ThermalAnalysis"

    @property
    def thermal_analysis(self: "CastSelf") -> "ThermalAnalysis":
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
class ThermalAnalysis(_0.APIBase):
    """ThermalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisTime")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_case(self: "Self") -> "_1503.ThermalLoadCase":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def setup(self: "Self") -> "_1481.ThermalElectricMachineSetup":
        """mastapy.electric_machines.thermal.ThermalElectricMachineSetup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Setup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def thermal_electric_machine(self: "Self") -> "_1480.ThermalElectricMachine":
        """mastapy.electric_machines.thermal.ThermalElectricMachine

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalElectricMachine")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def thermal_network(self: "Self") -> "_220.ThermalNetwork":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.ThermalNetwork

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalNetwork")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def thermal_results(self: "Self") -> "_1491.ThermalResults":
        """mastapy.electric_machines.thermal.results.ThermalResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def user_defined_nodes(
        self: "Self",
    ) -> "List[_226.UserDefinedNodeLoadCaseInformation]":
        """List[mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedNodeLoadCaseInformation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UserDefinedNodes")

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
    def create_electromagnetic_load_case(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateElectromagneticLoadCase")

    @exception_bridge
    def perform_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformAnalysis")

    @exception_bridge
    @enforce_parameter_types
    def perform_analysis_with_progress(
        self: "Self", task_progress: "_7901.TaskProgress"
    ) -> None:
        """Method does not return.

        Args:
            task_progress (mastapy.TaskProgress)
        """
        pythonnet_method_call(
            self.wrapped,
            "PerformAnalysisWithProgress",
            task_progress.wrapped if task_progress else None,
        )

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
    def cast_to(self: "Self") -> "_Cast_ThermalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_ThermalAnalysis
        """
        return _Cast_ThermalAnalysis(self)
