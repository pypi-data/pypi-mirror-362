"""ElectricMachineResultsForOpenCircuitAndOnLoad"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

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

_ELECTRIC_MACHINE_RESULTS_FOR_OPEN_CIRCUIT_AND_ON_LOAD = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results",
    "ElectricMachineResultsForOpenCircuitAndOnLoad",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.results import _1528, _1529
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="ElectricMachineResultsForOpenCircuitAndOnLoad")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineResultsForOpenCircuitAndOnLoad._Cast_ElectricMachineResultsForOpenCircuitAndOnLoad",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineResultsForOpenCircuitAndOnLoad",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineResultsForOpenCircuitAndOnLoad:
    """Special nested class for casting ElectricMachineResultsForOpenCircuitAndOnLoad to subclasses."""

    __parent__: "ElectricMachineResultsForOpenCircuitAndOnLoad"

    @property
    def electric_machine_results_for_open_circuit_and_on_load(
        self: "CastSelf",
    ) -> "ElectricMachineResultsForOpenCircuitAndOnLoad":
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
class ElectricMachineResultsForOpenCircuitAndOnLoad(_0.APIBase):
    """ElectricMachineResultsForOpenCircuitAndOnLoad

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_RESULTS_FOR_OPEN_CIRCUIT_AND_ON_LOAD

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def apparent_d_axis_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApparentDAxisInductance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_inductance_multiplied_by_current_d_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApparentInductanceMultipliedByCurrentDAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_inductance_multiplied_by_current_q_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApparentInductanceMultipliedByCurrentQAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_mutual_field_armature_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApparentMutualFieldArmatureInductance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def apparent_q_axis_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApparentQAxisInductance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_alignment_torque_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageAlignmentTorqueDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_reluctance_torque_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageReluctanceTorqueDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_speed_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseSpeedDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def current_angle_for_maximum_torque_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurrentAngleForMaximumTorqueDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_armature_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisArmatureFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electrical_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def line_line_inductance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LineLineInductance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def linear_dq_model_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearDQModelChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_angle_from_phasor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadAngleFromPhasor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_speed_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSpeedDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_torque_achievable_dq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTorqueAchievableDQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mechanical_time_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MechanicalTimeConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permanent_magnet_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermanentMagnetFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_reactive_voltage_drms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseReactiveVoltageDRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_reactive_voltage_qrms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseReactiveVoltageQRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_terminal_voltage_from_phasor_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhaseTerminalVoltageFromPhasorRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phasor_diagram(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PhasorDiagram")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def power_factor_angle_from_phasor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFactorAngleFromPhasor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_armature_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisArmatureFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def steady_state_short_circuit_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SteadyStateShortCircuitCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def on_load_results(self: "Self") -> "_1528.OnLoadElectricMachineResults":
        """mastapy.electric_machines.results.OnLoadElectricMachineResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OnLoadResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def open_circuit_results(self: "Self") -> "_1529.OpenCircuitElectricMachineResults":
        """mastapy.electric_machines.results.OpenCircuitElectricMachineResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenCircuitResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def all_on_load_results(self: "Self") -> "List[_1528.OnLoadElectricMachineResults]":
        """List[mastapy.electric_machines.results.OnLoadElectricMachineResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllOnLoadResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def all_open_circuit_results(
        self: "Self",
    ) -> "List[_1529.OpenCircuitElectricMachineResults]":
        """List[mastapy.electric_machines.results.OpenCircuitElectricMachineResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllOpenCircuitResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def on_load_results_for_slices(
        self: "Self",
    ) -> "List[_1528.OnLoadElectricMachineResults]":
        """List[mastapy.electric_machines.results.OnLoadElectricMachineResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OnLoadResultsForSlices")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def open_circuit_results_for_slices(
        self: "Self",
    ) -> "List[_1529.OpenCircuitElectricMachineResults]":
        """List[mastapy.electric_machines.results.OpenCircuitElectricMachineResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OpenCircuitResultsForSlices")

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineResultsForOpenCircuitAndOnLoad":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineResultsForOpenCircuitAndOnLoad
        """
        return _Cast_ElectricMachineResultsForOpenCircuitAndOnLoad(self)
