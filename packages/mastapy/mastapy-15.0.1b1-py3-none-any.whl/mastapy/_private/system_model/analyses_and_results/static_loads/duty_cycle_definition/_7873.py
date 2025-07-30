"""TimeSeriesImporter"""

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
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
    _7863,
)

_TIME_SERIES_IMPORTER = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.DutyCycleDefinition",
    "TimeSeriesImporter",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.static_loads import _7777
    from mastapy._private.system_model.analyses_and_results.static_loads.duty_cycle_definition import (
        _7861,
        _7862,
        _7864,
        _7865,
        _7866,
        _7867,
        _7868,
        _7872,
        _7874,
        _7875,
    )
    from mastapy._private.utility.file_access_helpers import _2014
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="TimeSeriesImporter")
    CastSelf = TypeVar("CastSelf", bound="TimeSeriesImporter._Cast_TimeSeriesImporter")


__docformat__ = "restructuredtext en"
__all__ = ("TimeSeriesImporter",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TimeSeriesImporter:
    """Special nested class for casting TimeSeriesImporter to subclasses."""

    __parent__: "TimeSeriesImporter"

    @property
    def time_series_importer(self: "CastSelf") -> "TimeSeriesImporter":
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
class TimeSeriesImporter(_0.APIBase):
    """TimeSeriesImporter

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TIME_SERIES_IMPORTER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def boost_pressure_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoostPressureChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def create_load_cases_for_parametric_study_tool(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CreateLoadCasesForParametricStudyTool"
        )

        if temp is None:
            return False

        return temp

    @create_load_cases_for_parametric_study_tool.setter
    @exception_bridge
    @enforce_parameter_types
    def create_load_cases_for_parametric_study_tool(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "CreateLoadCasesForParametricStudyTool",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def design_state_name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "DesignStateName")

        if temp is None:
            return ""

        return temp

    @design_state_name.setter
    @exception_bridge
    @enforce_parameter_types
    def design_state_name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "DesignStateName", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def destination_design_state_column(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.DestinationDesignState]"""
        temp = pythonnet_property_get(self.wrapped, "DestinationDesignStateColumn")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @destination_design_state_column.setter
    @exception_bridge
    @enforce_parameter_types
    def destination_design_state_column(
        self: "Self", value: "_7863.DestinationDesignState"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DestinationDesignState.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DestinationDesignStateColumn", value)

    @property
    @exception_bridge
    def duty_cycle_duration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DutyCycleDuration")

        if temp is None:
            return 0.0

        return temp

    @duty_cycle_duration.setter
    @exception_bridge
    @enforce_parameter_types
    def duty_cycle_duration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DutyCycleDuration",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def force_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_ratios(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatios")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def import_type(self: "Self") -> "_7777.ImportType":
        """mastapy.system_model.analyses_and_results.static_loads.ImportType"""
        temp = pythonnet_property_get(self.wrapped, "ImportType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ImportType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7777",
            "ImportType",
        )(value)

    @import_type.setter
    @exception_bridge
    @enforce_parameter_types
    def import_type(self: "Self", value: "_7777.ImportType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ImportType"
        )
        pythonnet_property_set(self.wrapped, "ImportType", value)

    @property
    @exception_bridge
    def moment_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def number_of_boost_pressure_inputs(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBoostPressureInputs")

        if temp is None:
            return 0

        return temp

    @number_of_boost_pressure_inputs.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_boost_pressure_inputs(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfBoostPressureInputs",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_cycle_repeats(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfCycleRepeats")

        if temp is None:
            return 0.0

        return temp

    @number_of_cycle_repeats.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_cycle_repeats(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfCycleRepeats",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_data_files(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfDataFiles")

        if temp is None:
            return 0

        return temp

    @number_of_data_files.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_data_files(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfDataFiles", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_extra_points_for_ramp_sections(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfExtraPointsForRampSections"
        )

        if temp is None:
            return 0

        return temp

    @number_of_extra_points_for_ramp_sections.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_extra_points_for_ramp_sections(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfExtraPointsForRampSections",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_force_inputs(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfForceInputs")

        if temp is None:
            return 0

        return temp

    @number_of_force_inputs.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_force_inputs(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfForceInputs", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_moment_inputs(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfMomentInputs")

        if temp is None:
            return 0

        return temp

    @number_of_moment_inputs.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_moment_inputs(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfMomentInputs", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_speed_inputs(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfSpeedInputs")

        if temp is None:
            return 0

        return temp

    @number_of_speed_inputs.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_speed_inputs(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfSpeedInputs", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_torque_inputs(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTorqueInputs")

        if temp is None:
            return 0

        return temp

    @number_of_torque_inputs.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_torque_inputs(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTorqueInputs", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def specify_load_case_names(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SpecifyLoadCaseNames")

        if temp is None:
            return False

        return temp

    @specify_load_case_names.setter
    @exception_bridge
    @enforce_parameter_types
    def specify_load_case_names(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifyLoadCaseNames",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def speed_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def torque_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def design_state_options(self: "Self") -> "_7862.DesignStateOptions":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.DesignStateOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignStateOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_ratio_options(self: "Self") -> "_7865.GearRatioInputOptions":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.GearRatioInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearRatioOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case_name_inputs(self: "Self") -> "_7866.LoadCaseNameOptions":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.LoadCaseNameOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseNameInputs")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_step_input(self: "Self") -> "_7874.TimeStepInputOptions":
        """mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.TimeStepInputOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeStepInput")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def boost_pressure_inputs(
        self: "Self",
    ) -> "List[_7861.BoostPressureLoadCaseInputOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.BoostPressureLoadCaseInputOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BoostPressureInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def file_inputs(self: "Self") -> "List[_7868.MultiTimeSeriesDataInputFileOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.MultiTimeSeriesDataInputFileOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FileInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_inputs(self: "Self") -> "List[_7864.ForceInputOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.ForceInputOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def moment_inputs(self: "Self") -> "List[_7867.MomentInputOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.MomentInputOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def speed_inputs(self: "Self") -> "List[_7872.SpeedInputOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.SpeedInputOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def torque_inputs(self: "Self") -> "List[_7875.TorqueInputOptions]":
        """List[mastapy.system_model.analyses_and_results.static_loads.duty_cycle_definition.TorqueInputOptions]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueInputs")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def columns(self: "Self") -> "List[_2014.ColumnTitle]":
        """List[mastapy.utility.file_access_helpers.ColumnTitle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Columns")

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
    def create_load_cases(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "CreateLoadCases")

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
    def cast_to(self: "Self") -> "_Cast_TimeSeriesImporter":
        """Cast to another type.

        Returns:
            _Cast_TimeSeriesImporter
        """
        return _Cast_TimeSeriesImporter(self)
