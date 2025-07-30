"""DIN7322010Results"""

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

_DIN7322010_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "DIN7322010Results"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="DIN7322010Results")
    CastSelf = TypeVar("CastSelf", bound="DIN7322010Results._Cast_DIN7322010Results")


__docformat__ = "restructuredtext en"
__all__ = ("DIN7322010Results",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DIN7322010Results:
    """Special nested class for casting DIN7322010Results to subclasses."""

    __parent__: "DIN7322010Results"

    @property
    def din7322010_results(self: "CastSelf") -> "DIN7322010Results":
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
class DIN7322010Results(_0.APIBase):
    """DIN7322010Results

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DIN7322010_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def air_convection_heat_dissipation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AirConvectionHeatDissipation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_equivalent_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicEquivalentLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def external_cooling_or_heating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalCoolingOrHeating")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def frictional_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrictionalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_dissipation_capacity_of_bearing_lubrication(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HeatDissipationCapacityOfBearingLubrication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heat_emitting_reference_surface_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeatEmittingReferenceSurfaceArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_speed_warning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingSpeedWarning")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def load_dependent_frictional_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadDependentFrictionalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def oil_dip_coefficient_f0_adjustment_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OilDipCoefficientF0AdjustmentFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_speed_warning(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedWarning")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def required_oil_flow_rate(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RequiredOilFlowRate")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_dependent_frictional_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedDependentFrictionalPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_limiting_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalLimitingSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_limiting_speed_f0(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalLimitingSpeedF0")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_limiting_speed_f1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalLimitingSpeedF1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_reference_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_reference_speed_f0r(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalReferenceSpeedF0r")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_reference_speed_f1r(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalReferenceSpeedF1r")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_heat_emitted(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalHeatEmitted")

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
    def cast_to(self: "Self") -> "_Cast_DIN7322010Results":
        """Cast to another type.

        Returns:
            _Cast_DIN7322010Results
        """
        return _Cast_DIN7322010Results(self)
