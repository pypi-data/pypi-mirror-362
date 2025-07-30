"""ThermalRotor"""

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
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_THERMAL_ROTOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalRotor"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1429
    from mastapy._private.electric_machines.thermal import _1461, _1469, _1473
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import (
        _208,
        _223,
    )

    Self = TypeVar("Self", bound="ThermalRotor")
    CastSelf = TypeVar("CastSelf", bound="ThermalRotor._Cast_ThermalRotor")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalRotor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalRotor:
    """Special nested class for casting ThermalRotor to subclasses."""

    __parent__: "ThermalRotor"

    @property
    def thermal_rotor(self: "CastSelf") -> "ThermalRotor":
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
class ThermalRotor(_0.APIBase):
    """ThermalRotor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_ROTOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def critical_reynolds_number(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CriticalReynoldsNumber")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @critical_reynolds_number.setter
    @exception_bridge
    @enforce_parameter_types
    def critical_reynolds_number(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CriticalReynoldsNumber", value)

    @property
    @exception_bridge
    def front_bearing_radial_thermal_resistance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "FrontBearingRadialThermalResistance"
        )

        if temp is None:
            return 0.0

        return temp

    @front_bearing_radial_thermal_resistance.setter
    @exception_bridge
    @enforce_parameter_types
    def front_bearing_radial_thermal_resistance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FrontBearingRadialThermalResistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def has_shaft_cooling_channel(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasShaftCoolingChannel")

        if temp is None:
            return False

        return temp

    @has_shaft_cooling_channel.setter
    @exception_bridge
    @enforce_parameter_types
    def has_shaft_cooling_channel(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasShaftCoolingChannel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def has_single_shaft_cooling_outlet(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HasSingleShaftCoolingOutlet")

        if temp is None:
            return False

        return temp

    @has_single_shaft_cooling_outlet.setter
    @exception_bridge
    @enforce_parameter_types
    def has_single_shaft_cooling_outlet(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HasSingleShaftCoolingOutlet",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def heat_transfer_coefficient_calculation_method(
        self: "Self",
    ) -> "_1469.HeatTransferCoefficientCalculationMethod":
        """mastapy.electric_machines.thermal.HeatTransferCoefficientCalculationMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientCalculationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.ElectricMachines.Thermal.HeatTransferCoefficientCalculationMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1469",
            "HeatTransferCoefficientCalculationMethod",
        )(value)

    @heat_transfer_coefficient_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def heat_transfer_coefficient_calculation_method(
        self: "Self", value: "_1469.HeatTransferCoefficientCalculationMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.ElectricMachines.Thermal.HeatTransferCoefficientCalculationMethod",
        )
        pythonnet_property_set(
            self.wrapped, "HeatTransferCoefficientCalculationMethod", value
        )

    @property
    @exception_bridge
    def inlet_position(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InletPosition")

        if temp is None:
            return 0.0

        return temp

    @inlet_position.setter
    @exception_bridge
    @enforce_parameter_types
    def inlet_position(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "InletPosition", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def interlaminate_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InterlaminateMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @interlaminate_material.setter
    @exception_bridge
    @enforce_parameter_types
    def interlaminate_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InterlaminateMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def nusselt_number_correlation_method(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NusseltNumberCorrelationMethod")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def rear_bearing_radial_thermal_resistance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RearBearingRadialThermalResistance"
        )

        if temp is None:
            return 0.0

        return temp

    @rear_bearing_radial_thermal_resistance.setter
    @exception_bridge
    @enforce_parameter_types
    def rear_bearing_radial_thermal_resistance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RearBearingRadialThermalResistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_bore(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftBore")

        if temp is None:
            return 0.0

        return temp

    @shaft_bore.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_bore(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftBore", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def shaft_coolant_fluid(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ShaftCoolantFluid", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @shaft_coolant_fluid.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_coolant_fluid(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ShaftCoolantFluid",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def shaft_cooling_inlet_location(self: "Self") -> "_1473.InletLocation":
        """mastapy.electric_machines.thermal.InletLocation"""
        temp = pythonnet_property_get(self.wrapped, "ShaftCoolingInletLocation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.ElectricMachines.Thermal.InletLocation"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.electric_machines.thermal._1473", "InletLocation"
        )(value)

    @shaft_cooling_inlet_location.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_cooling_inlet_location(
        self: "Self", value: "_1473.InletLocation"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.InletLocation"
        )
        pythonnet_property_set(self.wrapped, "ShaftCoolingInletLocation", value)

    @property
    @exception_bridge
    def shaft_front_extension_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftFrontExtensionLength")

        if temp is None:
            return 0.0

        return temp

    @shaft_front_extension_length.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_front_extension_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftFrontExtensionLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_front_extension_outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftFrontExtensionOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_front_extension_outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_front_extension_outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftFrontExtensionOuterDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_rear_extension_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftRearExtensionLength")

        if temp is None:
            return 0.0

        return temp

    @shaft_rear_extension_length.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_rear_extension_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftRearExtensionLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_rear_extension_outer_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftRearExtensionOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @shaft_rear_extension_outer_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_rear_extension_outer_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ShaftRearExtensionOuterDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specify_heat_transfer_coefficient_for_rotor_outer_boundary(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "SpecifyHeatTransferCoefficientForRotorOuterBoundary"
        )

        if temp is None:
            return False

        return temp

    @specify_heat_transfer_coefficient_for_rotor_outer_boundary.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_heat_transfer_coefficient_for_rotor_outer_boundary(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyHeatTransferCoefficientForRotorOuterBoundary",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def heat_transfer_coefficient_specification_for_shaft_cooling(
        self: "Self",
    ) -> "_223.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientSpecificationForShaftCooling"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor(self: "Self") -> "_1429.Rotor":
        """mastapy.electric_machines.Rotor

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rotor")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_outer_boundary_htc(
        self: "Self",
    ) -> "_223.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorOuterBoundaryHTC")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_to_magnet_interface_gap(self: "Self") -> "_208.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorToMagnetInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def rotor_to_shaft_interface_gap(self: "Self") -> "_208.InterfaceGap":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.InterfaceGap

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorToShaftInterfaceGap")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_channel(self: "Self") -> "_1461.Channel":
        """mastapy.electric_machines.thermal.Channel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftChannel")

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
    def cast_to(self: "Self") -> "_Cast_ThermalRotor":
        """Cast to another type.

        Returns:
            _Cast_ThermalRotor
        """
        return _Cast_ThermalRotor(self)
