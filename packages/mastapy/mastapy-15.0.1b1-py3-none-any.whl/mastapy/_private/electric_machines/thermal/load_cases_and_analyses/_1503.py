"""ThermalLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal.LoadCasesAndAnalyses", "ThermalLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.load_cases_and_analyses import _1540
    from mastapy._private.electric_machines.thermal import _1481
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses import (
        _1496,
        _1500,
        _1502,
        _1504,
    )
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _222

    Self = TypeVar("Self", bound="ThermalLoadCase")
    CastSelf = TypeVar("CastSelf", bound="ThermalLoadCase._Cast_ThermalLoadCase")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalLoadCase:
    """Special nested class for casting ThermalLoadCase to subclasses."""

    __parent__: "ThermalLoadCase"

    @property
    def thermal_load_case(self: "CastSelf") -> "ThermalLoadCase":
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
class ThermalLoadCase(_0.APIBase):
    """ThermalLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ambient_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AmbientTemperature")

        if temp is None:
            return 0.0

        return temp

    @ambient_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def ambient_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AmbientTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def electromagnetic_results_ready_string(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectromagneticResultsReadyString")

        if temp is None:
            return ""

        return temp

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
    def rotor_speed(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RotorSpeed")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @rotor_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def rotor_speed(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RotorSpeed", value)

    @property
    @exception_bridge
    def cooling_jacket(self: "Self") -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoolingJacket")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def front_inner_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontInnerCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def front_outer_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontOuterCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def front_side_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontSideCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case_group(self: "Self") -> "_1504.ThermalLoadCaseGroup":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCaseGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseGroup")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_losses(self: "Self") -> "_1500.PowerLosses":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.PowerLosses

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLosses")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rear_inner_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RearInnerCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rear_outer_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RearOuterCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rear_side_custom_end_winding_cooling(
        self: "Self",
    ) -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RearSideCustomEndWindingCooling")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_cooling_channels(self: "Self") -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorCoolingChannels")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_cooling_channel(self: "Self") -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftCoolingChannel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def solver_settings(self: "Self") -> "_222.ThermalNetworkSolverSettings":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.ThermalNetworkSolverSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SolverSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stator_cooling_channels(self: "Self") -> "_1496.CoolingLoadCaseSettings":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.CoolingLoadCaseSettings

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatorCoolingChannels")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def perform_electromagnetic_analysis(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformElectromagneticAnalysis")

    @exception_bridge
    @enforce_parameter_types
    def analysis_for(
        self: "Self", setup: "_1481.ThermalElectricMachineSetup"
    ) -> "_1502.ThermalAnalysis":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalAnalysis

        Args:
            setup (mastapy.electric_machines.thermal.ThermalElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "AnalysisFor", setup.wrapped if setup else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def copy_to(
        self: "Self", another_group: "_1504.ThermalLoadCaseGroup"
    ) -> "ThermalLoadCase":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase

        Args:
            another_group (mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCaseGroup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "CopyTo", another_group.wrapped if another_group else None
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def possible_electric_machine_fe_analyses(
        self: "Self",
    ) -> "List[_1540.ElectricMachineFEAnalysis]":
        """List[mastapy.electric_machines.load_cases_and_analyses.ElectricMachineFEAnalysis]"""
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(self.wrapped, "PossibleElectricMachineFEAnalyses")
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_analysis(
        self: "Self", electric_machine_thermal_analysis: "_1502.ThermalAnalysis"
    ) -> None:
        """Method does not return.

        Args:
            electric_machine_thermal_analysis (mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalAnalysis)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveAnalysis",
            electric_machine_thermal_analysis.wrapped
            if electric_machine_thermal_analysis
            else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_analysis_for(
        self: "Self", setup: "_1481.ThermalElectricMachineSetup"
    ) -> None:
        """Method does not return.

        Args:
            setup (mastapy.electric_machines.thermal.ThermalElectricMachineSetup)
        """
        pythonnet_method_call(
            self.wrapped, "RemoveAnalysisFor", setup.wrapped if setup else None
        )

    @exception_bridge
    @enforce_parameter_types
    def set_mapped_electromagnetic_analysis(
        self: "Self", analysis: "_1540.ElectricMachineFEAnalysis"
    ) -> None:
        """Method does not return.

        Args:
            analysis (mastapy.electric_machines.load_cases_and_analyses.ElectricMachineFEAnalysis)
        """
        pythonnet_method_call(
            self.wrapped,
            "SetMappedElectromagneticAnalysis",
            analysis.wrapped if analysis else None,
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
    def cast_to(self: "Self") -> "_Cast_ThermalLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ThermalLoadCase
        """
        return _Cast_ThermalLoadCase(self)
