"""ElectricMachineDQModel"""

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

_ELECTRIC_MACHINE_DQ_MODEL = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "ElectricMachineDQModel"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1451
    from mastapy._private.electric_machines.results import _1524, _1526

    Self = TypeVar("Self", bound="ElectricMachineDQModel")
    CastSelf = TypeVar(
        "CastSelf", bound="ElectricMachineDQModel._Cast_ElectricMachineDQModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDQModel",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineDQModel:
    """Special nested class for casting ElectricMachineDQModel to subclasses."""

    __parent__: "ElectricMachineDQModel"

    @property
    def linear_dq_model(self: "CastSelf") -> "_1524.LinearDQModel":
        from mastapy._private.electric_machines.results import _1524

        return self.__parent__._cast(_1524.LinearDQModel)

    @property
    def non_linear_dq_model(self: "CastSelf") -> "_1526.NonLinearDQModel":
        from mastapy._private.electric_machines.results import _1526

        return self.__parent__._cast(_1526.NonLinearDQModel)

    @property
    def electric_machine_dq_model(self: "CastSelf") -> "ElectricMachineDQModel":
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
class ElectricMachineDQModel(_0.APIBase):
    """ElectricMachineDQModel

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_DQ_MODEL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conductor_dimension_for_skin_depth_calculation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConductorDimensionForSkinDepthCalculation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def current_angle_to_maximise_torque_at_maximum_current_at_reference_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "CurrentAngleToMaximiseTorqueAtMaximumCurrentAtReferenceTemperature",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_phase_resistance_at_reference_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FieldWindingPhaseResistanceAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def field_winding_temperature_coefficient_for_winding_resistivity(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FieldWindingTemperatureCoefficientForWindingResistivity"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_peak_phase_current(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPeakPhaseCurrent")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_peak_phase_supply_voltage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPeakPhaseSupplyVoltage")

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
    def number_of_phases(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPhases")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_pole_pairs(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPolePairs")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def permanent_magnet_flux_linkage_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermanentMagnetFluxLinkageAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def phase_resistance_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PhaseResistanceAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def steady_state_short_circuit_current_at_reference_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SteadyStateShortCircuitCurrentAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def temperature_coefficient_for_remanence(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureCoefficientForRemanence"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def temperature_coefficient_for_winding_resistivity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureCoefficientForWindingResistivity"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_connection(self: "Self") -> "_1451.WindingConnection":
        """mastapy.electric_machines.WindingConnection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WindingConnection")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.WindingConnection"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines._1451", "WindingConnection"
        )(value)

    @property
    @exception_bridge
    def winding_material_relative_permeability_at_reference_temperature(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WindingMaterialRelativePermeabilityAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def winding_resistivity_at_reference_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WindingResistivityAtReferenceTemperature"
        )

        if temp is None:
            return 0.0

        return temp

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineDQModel":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineDQModel
        """
        return _Cast_ElectricMachineDQModel(self)
