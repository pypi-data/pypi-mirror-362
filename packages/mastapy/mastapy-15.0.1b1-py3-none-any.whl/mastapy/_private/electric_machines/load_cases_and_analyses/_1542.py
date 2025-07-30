"""ElectricMachineLoadCase"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.electric_machines.load_cases_and_analyses import _1543
from mastapy._private.nodal_analysis.elmer import _249

_ELECTRIC_MACHINE_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineLoadCase"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.electric_machines import _1394
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1540,
        _1546,
        _1560,
    )

    Self = TypeVar("Self", bound="ElectricMachineLoadCase")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineLoadCase._Cast_ElectricMachineLoadCase"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineLoadCase:
    """Special nested class for casting ElectricMachineLoadCase to subclasses."""

    __parent__: "ElectricMachineLoadCase"

    @property
    def electric_machine_load_case_base(
        self: "CastSelf",
    ) -> "_1543.ElectricMachineLoadCaseBase":
        return self.__parent__._cast(_1543.ElectricMachineLoadCaseBase)

    @property
    def speed_torque_load_case(self: "CastSelf") -> "_1560.SpeedTorqueLoadCase":
        from mastapy._private.electric_machines.load_cases_and_analyses import _1560

        return self.__parent__._cast(_1560.SpeedTorqueLoadCase)

    @property
    def electric_machine_load_case(self: "CastSelf") -> "ElectricMachineLoadCase":
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
class ElectricMachineLoadCase(_1543.ElectricMachineLoadCaseBase):
    """ElectricMachineLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_period(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod":
        """EnumWithSelectedValue[mastapy.nodal_analysis.elmer.ElectricMachineAnalysisPeriod]"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisPeriod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @analysis_period.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_period(
        self: "Self", value: "_249.ElectricMachineAnalysisPeriod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ElectricMachineAnalysisPeriod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "AnalysisPeriod", value)

    @property
    @exception_bridge
    def core_loss_minor_loop_hysteresis_loss_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "CoreLossMinorLoopHysteresisLossFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @core_loss_minor_loop_hysteresis_loss_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def core_loss_minor_loop_hysteresis_loss_factor(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CoreLossMinorLoopHysteresisLossFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def current_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CurrentAngle")

        if temp is None:
            return 0.0

        return temp

    @current_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def current_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "CurrentAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def end_winding_inductance_method(
        self: "Self",
    ) -> "_1546.EndWindingInductanceMethod":
        """mastapy.electric_machines.load_cases_and_analyses.EndWindingInductanceMethod"""
        temp = pythonnet_property_get(self.wrapped, "EndWindingInductanceMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.EndWindingInductanceMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.load_cases_and_analyses._1546",
            "EndWindingInductanceMethod",
        )(value)

    @end_winding_inductance_method.setter
    @exception_bridge
    @enforce_parameter_types
    def end_winding_inductance_method(
        self: "Self", value: "_1546.EndWindingInductanceMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.EndWindingInductanceMethod",
        )
        pythonnet_property_set(self.wrapped, "EndWindingInductanceMethod", value)

    @property
    @exception_bridge
    def field_winding_current(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FieldWindingCurrent")

        if temp is None:
            return 0.0

        return temp

    @field_winding_current.setter
    @exception_bridge
    @enforce_parameter_types
    def field_winding_current(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FieldWindingCurrent",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_iron_and_eddy_current_losses(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeIronAndEddyCurrentLosses")

        if temp is None:
            return False

        return temp

    @include_iron_and_eddy_current_losses.setter
    @exception_bridge
    @enforce_parameter_types
    def include_iron_and_eddy_current_losses(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeIronAndEddyCurrentLosses",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_open_circuit_calculation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeOpenCircuitCalculation")

        if temp is None:
            return False

        return temp

    @include_open_circuit_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def include_open_circuit_calculation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeOpenCircuitCalculation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_winding_ac_losses(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeWindingACLosses")

        if temp is None:
            return False

        return temp

    @include_winding_ac_losses.setter
    @exception_bridge
    @enforce_parameter_types
    def include_winding_ac_losses(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeWindingACLosses",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def minimum_number_of_steps_for_voltages_and_losses_calculation(
        self: "Self",
    ) -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfStepsForVoltagesAndLossesCalculation"
        )

        if temp is None:
            return 0

        return temp

    @minimum_number_of_steps_for_voltages_and_losses_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_steps_for_voltages_and_losses_calculation(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumNumberOfStepsForVoltagesAndLossesCalculation",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def non_linear_relaxation_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NonLinearRelaxationFactor")

        if temp is None:
            return 0.0

        return temp

    @non_linear_relaxation_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_relaxation_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearRelaxationFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_system_convergence_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearSystemConvergenceTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_system_convergence_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_system_convergence_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearSystemConvergenceTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_system_maximum_number_of_iterations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearSystemMaximumNumberOfIterations"
        )

        if temp is None:
            return 0

        return temp

    @non_linear_system_maximum_number_of_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_system_maximum_number_of_iterations(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearSystemMaximumNumberOfIterations",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_cycles(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCycles")

        if temp is None:
            return 0

        return temp

    @number_of_cycles.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycles(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfCycles", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_initial_transient_steps(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfInitialTransientSteps")

        if temp is None:
            return 0

        return temp

    @number_of_initial_transient_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_initial_transient_steps(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfInitialTransientSteps",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_steps_per_analysis_period(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsPerAnalysisPeriod")

        if temp is None:
            return 0

        return temp

    @number_of_steps_per_analysis_period.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps_per_analysis_period(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStepsPerAnalysisPeriod",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def override_design_end_winding_inductance_method(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "OverrideDesignEndWindingInductanceMethod"
        )

        if temp is None:
            return False

        return temp

    @override_design_end_winding_inductance_method.setter
    @exception_bridge
    @enforce_parameter_types
    def override_design_end_winding_inductance_method(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OverrideDesignEndWindingInductanceMethod",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def peak_line_current(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PeakLineCurrent")

        if temp is None:
            return 0.0

        return temp

    @peak_line_current.setter
    @exception_bridge
    @enforce_parameter_types
    def peak_line_current(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PeakLineCurrent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rms_line_current(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RMSLineCurrent")

        if temp is None:
            return 0.0

        return temp

    @rms_line_current.setter
    @exception_bridge
    @enforce_parameter_types
    def rms_line_current(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RMSLineCurrent", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Speed")

        if temp is None:
            return 0.0

        return temp

    @speed.setter
    @exception_bridge
    @enforce_parameter_types
    def speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Speed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def total_number_of_time_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalNumberOfTimeSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def user_specified_end_winding_inductance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "UserSpecifiedEndWindingInductance")

        if temp is None:
            return 0.0

        return temp

    @user_specified_end_winding_inductance.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_end_winding_inductance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedEndWindingInductance",
            float(value) if value is not None else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def analysis_for(
        self: "Self", setup: "_1394.ElectricMachineSetup"
    ) -> "_1540.ElectricMachineFEAnalysis":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineFEAnalysis

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
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

    @property
    def cast_to(self: "Self") -> "_Cast_ElectricMachineLoadCase":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineLoadCase
        """
        return _Cast_ElectricMachineLoadCase(self)
