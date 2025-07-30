"""ThermalWindings"""

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
_THERMAL_WINDINGS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "ThermalWindings"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ThermalWindings")
    CastSelf = TypeVar("CastSelf", bound="ThermalWindings._Cast_ThermalWindings")


__docformat__ = "restructuredtext en"
__all__ = ("ThermalWindings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalWindings:
    """Special nested class for casting ThermalWindings to subclasses."""

    __parent__: "ThermalWindings"

    @property
    def thermal_windings(self: "CastSelf") -> "ThermalWindings":
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
class ThermalWindings(_0.APIBase):
    """ThermalWindings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_WINDINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_coil_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageCoilPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_axial_thermal_conductivity(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentAxialThermalConductivity"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @equivalent_axial_thermal_conductivity.setter
    @exception_bridge
    @enforce_parameter_types
    def equivalent_axial_thermal_conductivity(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "EquivalentAxialThermalConductivity", value
        )

    @property
    @exception_bridge
    def equivalent_density(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EquivalentDensity")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @equivalent_density.setter
    @exception_bridge
    @enforce_parameter_types
    def equivalent_density(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EquivalentDensity", value)

    @property
    @exception_bridge
    def equivalent_radial_thermal_conductivity(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "EquivalentRadialThermalConductivity"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @equivalent_radial_thermal_conductivity.setter
    @exception_bridge
    @enforce_parameter_types
    def equivalent_radial_thermal_conductivity(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "EquivalentRadialThermalConductivity", value
        )

    @property
    @exception_bridge
    def equivalent_specific_heat(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "EquivalentSpecificHeat")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @equivalent_specific_heat.setter
    @exception_bridge
    @enforce_parameter_types
    def equivalent_specific_heat(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "EquivalentSpecificHeat", value)

    @property
    @exception_bridge
    def impregnation_goodness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ImpregnationGoodness")

        if temp is None:
            return 0.0

        return temp

    @impregnation_goodness.setter
    @exception_bridge
    @enforce_parameter_types
    def impregnation_goodness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ImpregnationGoodness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def impregnation_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ImpregnationMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @impregnation_material.setter
    @exception_bridge
    @enforce_parameter_types
    def impregnation_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ImpregnationMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def insulation_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InsulationThickness")

        if temp is None:
            return 0.0

        return temp

    @insulation_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def insulation_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InsulationThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def length_of_straight_extension(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LengthOfStraightExtension")

        if temp is None:
            return 0.0

        return temp

    @length_of_straight_extension.setter
    @exception_bridge
    @enforce_parameter_types
    def length_of_straight_extension(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LengthOfStraightExtension",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_elements_in_radial_direction(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfElementsInRadialDirection")

        if temp is None:
            return 0

        return temp

    @number_of_elements_in_radial_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_elements_in_radial_direction(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfElementsInRadialDirection",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_elements_in_tangential_direction(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfElementsInTangentialDirection"
        )

        if temp is None:
            return 0

        return temp

    @number_of_elements_in_tangential_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_elements_in_tangential_direction(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfElementsInTangentialDirection",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def temperature_for_air_pockets_in_impregnation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "TemperatureForAirPocketsInImpregnation"
        )

        if temp is None:
            return 0.0

        return temp

    @temperature_for_air_pockets_in_impregnation.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_for_air_pockets_in_impregnation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureForAirPocketsInImpregnation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def winding_insulation_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "WindingInsulationMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @winding_insulation_material.setter
    @exception_bridge
    @enforce_parameter_types
    def winding_insulation_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "WindingInsulationMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

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
    def cast_to(self: "Self") -> "_Cast_ThermalWindings":
        """Cast to another type.

        Returns:
            _Cast_ThermalWindings
        """
        return _Cast_ThermalWindings(self)
