"""CoolingChannelForThermalAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    overridable_enum_runtime,
    utility,
)
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
from mastapy._private.electric_machines import _1378

_COOLING_CHANNEL_FOR_THERMAL_ANALYSIS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal", "CoolingChannelForThermalAnalysis"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal import _1461, _1469, _1473
    from mastapy._private.nodal_analysis.lumped_parameter_thermal_analysis import _223

    Self = TypeVar("Self", bound="CoolingChannelForThermalAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoolingChannelForThermalAnalysis._Cast_CoolingChannelForThermalAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoolingChannelForThermalAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CoolingChannelForThermalAnalysis:
    """Special nested class for casting CoolingChannelForThermalAnalysis to subclasses."""

    __parent__: "CoolingChannelForThermalAnalysis"

    @property
    def cooling_channel_for_thermal_analysis(
        self: "CastSelf",
    ) -> "CoolingChannelForThermalAnalysis":
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
class CoolingChannelForThermalAnalysis(_0.APIBase):
    """CoolingChannelForThermalAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _COOLING_CHANNEL_FOR_THERMAL_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def channel_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def channel_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def channel_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChannelWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cooling_channel_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoolingChannelDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cooling_channel_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def cooling_channel_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoolingChannelDiameter", value)

    @property
    @exception_bridge
    def cooling_channel_height(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoolingChannelHeight")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cooling_channel_height.setter
    @exception_bridge
    @enforce_parameter_types
    def cooling_channel_height(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoolingChannelHeight", value)

    @property
    @exception_bridge
    def cooling_channel_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CoolingChannelWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cooling_channel_width.setter
    @exception_bridge
    @enforce_parameter_types
    def cooling_channel_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CoolingChannelWidth", value)

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
    def inlet_location(self: "Self") -> "_1473.InletLocation":
        """mastapy.electric_machines.thermal.InletLocation"""
        temp = pythonnet_property_get(self.wrapped, "InletLocation")

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

    @inlet_location.setter
    @exception_bridge
    @enforce_parameter_types
    def inlet_location(self: "Self", value: "_1473.InletLocation") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.ElectricMachines.Thermal.InletLocation"
        )
        pythonnet_property_set(self.wrapped, "InletLocation", value)

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
    def shape(self: "Self") -> "overridable.Overridable_CoolingChannelShape":
        """Overridable[mastapy.electric_machines.CoolingChannelShape]"""
        temp = pythonnet_property_get(self.wrapped, "Shape")

        if temp is None:
            return None

        value = overridable.Overridable_CoolingChannelShape.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @shape.setter
    @exception_bridge
    @enforce_parameter_types
    def shape(
        self: "Self",
        value: "Union[_1378.CoolingChannelShape, Tuple[_1378.CoolingChannelShape, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_CoolingChannelShape.wrapper_type()
        enclosed_type = overridable.Overridable_CoolingChannelShape.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Shape", value)

    @property
    @exception_bridge
    def channel(self: "Self") -> "_1461.Channel":
        """mastapy.electric_machines.thermal.Channel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Channel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def heat_transfer_coefficient_specification(
        self: "Self",
    ) -> "_223.UserDefinedHeatTransferCoefficient":
        """mastapy.nodal_analysis.lumped_parameter_thermal_analysis.UserDefinedHeatTransferCoefficient

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeatTransferCoefficientSpecification"
        )

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
    def cast_to(self: "Self") -> "_Cast_CoolingChannelForThermalAnalysis":
        """Cast to another type.

        Returns:
            _Cast_CoolingChannelForThermalAnalysis
        """
        return _Cast_CoolingChannelForThermalAnalysis(self)
