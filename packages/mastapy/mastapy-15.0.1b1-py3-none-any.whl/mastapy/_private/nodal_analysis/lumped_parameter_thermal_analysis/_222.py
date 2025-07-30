"""ThermalNetworkSolverSettings"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_THERMAL_NETWORK_SOLVER_SETTINGS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.LumpedParameterThermalAnalysis",
    "ThermalNetworkSolverSettings",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ThermalNetworkSolverSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ThermalNetworkSolverSettings._Cast_ThermalNetworkSolverSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalNetworkSolverSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalNetworkSolverSettings:
    """Special nested class for casting ThermalNetworkSolverSettings to subclasses."""

    __parent__: "ThermalNetworkSolverSettings"

    @property
    def thermal_network_solver_settings(
        self: "CastSelf",
    ) -> "ThermalNetworkSolverSettings":
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
class ThermalNetworkSolverSettings(_0.APIBase):
    """ThermalNetworkSolverSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_NETWORK_SOLVER_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_tolerance_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AbsoluteTolerancePressure")

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteTolerancePressure",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AbsoluteToleranceTemperature")

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def absolute_tolerance_volumetric_flow_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AbsoluteToleranceVolumetricFlowRate"
        )

        if temp is None:
            return 0.0

        return temp

    @absolute_tolerance_volumetric_flow_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def absolute_tolerance_volumetric_flow_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AbsoluteToleranceVolumetricFlowRate",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_number_of_iterations(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfIterations")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_iterations.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_iterations(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumNumberOfIterations",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def power_absolute_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PowerAbsoluteTolerance")

        if temp is None:
            return 0.0

        return temp

    @power_absolute_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def power_absolute_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PowerAbsoluteTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def power_relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PowerRelativeTolerance")

        if temp is None:
            return 0.0

        return temp

    @power_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def power_relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PowerRelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_absolute_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAbsoluteTolerance")

        if temp is None:
            return 0.0

        return temp

    @pressure_absolute_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_absolute_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAbsoluteTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureRelativeTolerance")

        if temp is None:
            return 0.0

        return temp

    @pressure_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureRelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RelativeTolerance")

        if temp is None:
            return 0.0

        return temp

    @relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relaxation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Relaxation")

        if temp is None:
            return 0.0

        return temp

    @relaxation.setter
    @exception_bridge
    @enforce_parameter_types
    def relaxation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Relaxation", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def residual_pressure_and_volumetric_flow_rate_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ResidualPressureAndVolumetricFlowRateTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @residual_pressure_and_volumetric_flow_rate_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_pressure_and_volumetric_flow_rate_tolerance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualPressureAndVolumetricFlowRateTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_relative_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResidualRelativeTolerance")

        if temp is None:
            return 0.0

        return temp

    @residual_relative_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_relative_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualRelativeTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def residual_temperature_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ResidualTemperatureTolerance")

        if temp is None:
            return 0.0

        return temp

    @residual_temperature_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def residual_temperature_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ResidualTemperatureTolerance",
            float(value) if value is not None else 0.0,
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
    def cast_to(self: "Self") -> "_Cast_ThermalNetworkSolverSettings":
        """Cast to another type.

        Returns:
            _Cast_ThermalNetworkSolverSettings
        """
        return _Cast_ThermalNetworkSolverSettings(self)
