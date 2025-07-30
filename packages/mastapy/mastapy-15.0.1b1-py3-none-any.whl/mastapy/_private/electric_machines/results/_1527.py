"""NonLinearDQModelGeneratorSettings"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.nodal_analysis.elmer import _249

_NON_LINEAR_DQ_MODEL_GENERATOR_SETTINGS = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Results", "NonLinearDQModelGeneratorSettings"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.load_cases_and_analyses import _1561

    Self = TypeVar("Self", bound="NonLinearDQModelGeneratorSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NonLinearDQModelGeneratorSettings._Cast_NonLinearDQModelGeneratorSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NonLinearDQModelGeneratorSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_NonLinearDQModelGeneratorSettings:
    """Special nested class for casting NonLinearDQModelGeneratorSettings to subclasses."""

    __parent__: "NonLinearDQModelGeneratorSettings"

    @property
    def non_linear_dq_model_generator_settings(
        self: "CastSelf",
    ) -> "NonLinearDQModelGeneratorSettings":
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
class NonLinearDQModelGeneratorSettings(_0.APIBase):
    """NonLinearDQModelGeneratorSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _NON_LINEAR_DQ_MODEL_GENERATOR_SETTINGS

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
    def copy_all_setups(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CopyAllSetups")

        if temp is None:
            return False

        return temp

    @copy_all_setups.setter
    @exception_bridge
    @enforce_parameter_types
    def copy_all_setups(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "CopyAllSetups", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def exponent_for_ac_winding_loss_temperature_scaling(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ExponentForACWindingLossTemperatureScaling"
        )

        if temp is None:
            return 0.0

        return temp

    @exponent_for_ac_winding_loss_temperature_scaling.setter
    @exception_bridge
    @enforce_parameter_types
    def exponent_for_ac_winding_loss_temperature_scaling(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ExponentForACWindingLossTemperatureScaling",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_ac_winding_losses(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeACWindingLosses")

        if temp is None:
            return False

        return temp

    @include_ac_winding_losses.setter
    @exception_bridge
    @enforce_parameter_types
    def include_ac_winding_losses(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeACWindingLosses",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_efficiency(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeEfficiency")

        if temp is None:
            return False

        return temp

    @include_efficiency.setter
    @exception_bridge
    @enforce_parameter_types
    def include_efficiency(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeEfficiency",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def maximum_current_angle_for_map(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumCurrentAngleForMap")

        if temp is None:
            return 0.0

        return temp

    @maximum_current_angle_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_current_angle_for_map(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumCurrentAngleForMap",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_field_winding_current_for_map(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumFieldWindingCurrentForMap")

        if temp is None:
            return 0.0

        return temp

    @maximum_field_winding_current_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_field_winding_current_for_map(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumFieldWindingCurrentForMap",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_peak_line_current_magnitude_for_map(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPeakLineCurrentMagnitudeForMap"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_peak_line_current_magnitude_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_peak_line_current_magnitude_for_map(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumPeakLineCurrentMagnitudeForMap", value
        )

    @property
    @exception_bridge
    def minimum_current_angle_for_map(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumCurrentAngleForMap")

        if temp is None:
            return 0.0

        return temp

    @minimum_current_angle_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_current_angle_for_map(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumCurrentAngleForMap",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_field_winding_current_for_map(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumFieldWindingCurrentForMap")

        if temp is None:
            return 0.0

        return temp

    @minimum_field_winding_current_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_field_winding_current_for_map(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumFieldWindingCurrentForMap",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_peak_line_current_magnitude_for_map(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumPeakLineCurrentMagnitudeForMap"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_peak_line_current_magnitude_for_map.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_peak_line_current_magnitude_for_map(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumPeakLineCurrentMagnitudeForMap",
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
    def number_of_current_angle_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCurrentAnglePoints")

        if temp is None:
            return 0

        return temp

    @number_of_current_angle_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_current_angle_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCurrentAnglePoints",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_current_magnitude_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCurrentMagnitudePoints")

        if temp is None:
            return 0

        return temp

    @number_of_current_magnitude_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_current_magnitude_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCurrentMagnitudePoints",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_field_winding_current_points(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfFieldWindingCurrentPoints")

        if temp is None:
            return 0

        return temp

    @number_of_field_winding_current_points.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_field_winding_current_points(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfFieldWindingCurrentPoints",
            int(value) if value is not None else 0,
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
    def number_of_time_steps_for_analysis_period(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfTimeStepsForAnalysisPeriod"
        )

        if temp is None:
            return 0

        return temp

    @number_of_time_steps_for_analysis_period.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_time_steps_for_analysis_period(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTimeStepsForAnalysisPeriod",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def reference_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeed")

        if temp is None:
            return 0.0

        return temp

    @reference_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def reference_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ReferenceSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def temperatures(self: "Self") -> "_1561.Temperatures":
        """mastapy.electric_machines.load_cases_and_analyses.Temperatures

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Temperatures")

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
    def cast_to(self: "Self") -> "_Cast_NonLinearDQModelGeneratorSettings":
        """Cast to another type.

        Returns:
            _Cast_NonLinearDQModelGeneratorSettings
        """
        return _Cast_NonLinearDQModelGeneratorSettings(self)
