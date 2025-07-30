"""ElectricMachineResultsTimeStep"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_2d import Vector2D

_ELECTRIC_MACHINE_RESULTS_TIME_STEP = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "ElectricMachineResultsTimeStep"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.results import _1516, _1517, _1518, _1520
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="ElectricMachineResultsTimeStep")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineResultsTimeStep._Cast_ElectricMachineResultsTimeStep",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineResultsTimeStep",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineResultsTimeStep:
    """Special nested class for casting ElectricMachineResultsTimeStep to subclasses."""

    __parent__: "ElectricMachineResultsTimeStep"

    @property
    def electric_machine_results_time_step(
        self: "CastSelf",
    ) -> "ElectricMachineResultsTimeStep":
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
class ElectricMachineResultsTimeStep(_0.APIBase):
    """ElectricMachineResultsTimeStep

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_RESULTS_TIME_STEP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ac_winding_loss(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ACWindingLoss")

        if temp is None:
            return 0.0

        return temp

    @ac_winding_loss.setter
    @exception_bridge
    @enforce_parameter_types
    def ac_winding_loss(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ACWindingLoss", float(value) if value is not None else 0.0
        )

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
    def d_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_reactive_voltages(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisReactiveVoltages")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_resistive_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisResistiveVoltage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def d_axis_terminal_voltages(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DAxisTerminalVoltages")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def electrical_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElectricalAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flux_density_in_air_gap_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FluxDensityInAirGapChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_density_in_air_gap_mst_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceDensityInAirGapMSTChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def mechanical_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MechanicalAngle")

        if temp is None:
            return 0.0

        return temp

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
    def q_axis_flux_linkage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisFluxLinkage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_reactive_voltages(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisReactiveVoltages")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_resistive_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisResistiveVoltage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def q_axis_terminal_voltages(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QAxisTerminalVoltages")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rotor_resultant_x_force_mst_single_contour(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RotorResultantXForceMSTSingleContour"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rotor_resultant_y_force_mst_single_contour(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RotorResultantYForceMSTSingleContour"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Time")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_index(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeIndex")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def torque_from_stator_tooth_tangential_forces(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TorqueFromStatorToothTangentialForces"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_mst_single_contour(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueMSTSingleContour")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_mst(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueMST")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def results_for_stator_teeth(
        self: "Self",
    ) -> "List[_1517.ElectricMachineResultsForStatorToothAtTimeStep]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsForStatorToothAtTimeStep]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForStatorTeeth")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def results_at_locations(
        self: "Self",
    ) -> "List[_1520.ElectricMachineResultsTimeStepAtLocation]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsTimeStepAtLocation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsAtLocations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def results_for_line_to_line(
        self: "Self",
    ) -> "List[_1518.ElectricMachineResultsLineToLineAtTimeStep]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsLineToLineAtTimeStep]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForLineToLine")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def results_for_phases(
        self: "Self",
    ) -> "List[_1516.ElectricMachineResultsForPhaseAtTimeStep]":
        """List[mastapy.electric_machines.results.ElectricMachineResultsForPhaseAtTimeStep]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForPhases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def elemental_flux_densities(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementalFluxDensities")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def magnetic_vector_potential(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MagneticVectorPotential")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def nodal_positions(self: "Self") -> "List[Vector2D]":
        """List[Vector2D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodalPositions")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector2D)

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
    def elements_node_id_for(self: "Self", node_number: "int") -> "List[int]":
        """List[int]

        Args:
            node_number (int)
        """
        node_number = int(node_number)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped, "ElementsNodeIDFor", node_number if node_number else 0
            ),
            int,
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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineResultsTimeStep":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineResultsTimeStep
        """
        return _Cast_ElectricMachineResultsTimeStep(self)
