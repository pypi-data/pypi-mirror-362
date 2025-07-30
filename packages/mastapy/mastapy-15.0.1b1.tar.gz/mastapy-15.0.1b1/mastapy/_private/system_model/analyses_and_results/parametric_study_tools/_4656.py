"""ParametricStudyToolOptions"""

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
from mastapy._private._internal.implicit import (
    enum_with_selected_value,
    list_with_selected_item,
    overridable,
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7686

_PARAMETRIC_STUDY_TOOL_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyToolOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility.convergence import _1760
    from mastapy._private.system_model import _2414, _2419
    from mastapy._private.system_model.analyses_and_results import _2889
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4658,
        _4659,
        _4660,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7798

    Self = TypeVar("Self", bound="ParametricStudyToolOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyToolOptions._Cast_ParametricStudyToolOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyToolOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyToolOptions:
    """Special nested class for casting ParametricStudyToolOptions to subclasses."""

    __parent__: "ParametricStudyToolOptions"

    @property
    def parametric_study_tool_options(self: "CastSelf") -> "ParametricStudyToolOptions":
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
class ParametricStudyToolOptions(_0.APIBase):
    """ParametricStudyToolOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_TOOL_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_AnalysisType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.static_loads.AnalysisType]"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisType")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_AnalysisType.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @analysis_type.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_type(self: "Self", value: "_7686.AnalysisType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = (
            enum_with_selected_value.EnumWithSelectedValue_AnalysisType.implicit_type()
        )
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "AnalysisType", value)

    @property
    @exception_bridge
    def changing_design(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ChangingDesign")

        if temp is None:
            return False

        return temp

    @changing_design.setter
    @exception_bridge
    @enforce_parameter_types
    def changing_design(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ChangingDesign", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def folder_path_for_saved_files(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FolderPathForSavedFiles")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def is_logging_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsLoggingData")

        if temp is None:
            return False

        return temp

    @is_logging_data.setter
    @exception_bridge
    @enforce_parameter_types
    def is_logging_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsLoggingData", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def log_report(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "LogReport")

        if temp is None:
            return False

        return temp

    @log_report.setter
    @exception_bridge
    @enforce_parameter_types
    def log_report(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "LogReport", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def maximum_number_of_design_copies_to_use(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfDesignCopiesToUse")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @maximum_number_of_design_copies_to_use.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_design_copies_to_use(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumNumberOfDesignCopiesToUse", value)

    @property
    @exception_bridge
    def number_of_analysis_dimensions(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfAnalysisDimensions")

        if temp is None:
            return 0

        return temp

    @number_of_analysis_dimensions.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_analysis_dimensions(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfAnalysisDimensions",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_steps(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfSteps")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def parametric_study_type(self: "Self") -> "_7798.ParametricStudyType":
        """mastapy.system_model.analyses_and_results.static_loads.ParametricStudyType"""
        temp = pythonnet_property_get(self.wrapped, "ParametricStudyType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ParametricStudyType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7798",
            "ParametricStudyType",
        )(value)

    @parametric_study_type.setter
    @exception_bridge
    @enforce_parameter_types
    def parametric_study_type(self: "Self", value: "_7798.ParametricStudyType") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.ParametricStudyType",
        )
        pythonnet_property_set(self.wrapped, "ParametricStudyType", value)

    @property
    @exception_bridge
    def perform_system_optimisation_pst_post_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "PerformSystemOptimisationPSTPostAnalysis"
        )

        if temp is None:
            return False

        return temp

    @perform_system_optimisation_pst_post_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def perform_system_optimisation_pst_post_analysis(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PerformSystemOptimisationPSTPostAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def put_newly_added_numerical_variables_into(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_str":
        """ListWithSelectedItem[str]"""
        temp = pythonnet_property_get(
            self.wrapped, "PutNewlyAddedNumericalVariablesInto"
        )

        if temp is None:
            return ""

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_str",
        )(temp)

    @put_newly_added_numerical_variables_into.setter
    @exception_bridge
    @enforce_parameter_types
    def put_newly_added_numerical_variables_into(self: "Self", value: "str") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_str.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped, "PutNewlyAddedNumericalVariablesInto", value
        )

    @property
    @exception_bridge
    def save_design_at_each_step(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SaveDesignAtEachStep")

        if temp is None:
            return False

        return temp

    @save_design_at_each_step.setter
    @exception_bridge
    @enforce_parameter_types
    def save_design_at_each_step(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SaveDesignAtEachStep",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def save_step_results_during_simulation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "SaveStepResultsDuringSimulation")

        if temp is None:
            return False

        return temp

    @save_step_results_during_simulation.setter
    @exception_bridge
    @enforce_parameter_types
    def save_step_results_during_simulation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SaveStepResultsDuringSimulation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def step_save_method(self: "Self") -> "_4659.ParametricStudyToolStepSaveMethod":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolStepSaveMethod"""
        temp = pythonnet_property_get(self.wrapped, "StepSaveMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.ParametricStudyToolStepSaveMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.parametric_study_tools._4659",
            "ParametricStudyToolStepSaveMethod",
        )(value)

    @step_save_method.setter
    @exception_bridge
    @enforce_parameter_types
    def step_save_method(
        self: "Self", value: "_4659.ParametricStudyToolStepSaveMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools.ParametricStudyToolStepSaveMethod",
        )
        pythonnet_property_set(self.wrapped, "StepSaveMethod", value)

    @property
    @exception_bridge
    def steps_for_statistical_study(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "StepsForStatisticalStudy")

        if temp is None:
            return 0

        return temp

    @steps_for_statistical_study.setter
    @exception_bridge
    @enforce_parameter_types
    def steps_for_statistical_study(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StepsForStatisticalStudy",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def steps_in_dimension_1(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "StepsInDimension1")

        if temp is None:
            return 0

        return temp

    @steps_in_dimension_1.setter
    @exception_bridge
    @enforce_parameter_types
    def steps_in_dimension_1(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "StepsInDimension1", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def steps_in_dimension_2(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "StepsInDimension2")

        if temp is None:
            return 0

        return temp

    @steps_in_dimension_2.setter
    @exception_bridge
    @enforce_parameter_types
    def steps_in_dimension_2(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "StepsInDimension2", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def use_multiple_designs(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseMultipleDesigns")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_multiple_designs.setter
    @exception_bridge
    @enforce_parameter_types
    def use_multiple_designs(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseMultipleDesigns", value)

    @property
    @exception_bridge
    def write_run_input_information_to_text_file(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "WriteRunInputInformationToTextFile"
        )

        if temp is None:
            return False

        return temp

    @write_run_input_information_to_text_file.setter
    @exception_bridge
    @enforce_parameter_types
    def write_run_input_information_to_text_file(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WriteRunInputInformationToTextFile",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def external_full_fe_loader(self: "Self") -> "_2419.ExternalFullFELoader":
        """mastapy.system_model.ExternalFullFELoader

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExternalFullFELoader")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def step_results(self: "Self") -> "List[_4658.ParametricStudyToolStepResult]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolStepResult]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StepResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def study_variables(self: "Self") -> "List[_4660.ParametricStudyVariable]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StudyVariables")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def parametric_study_logging_variables(
        self: "Self",
    ) -> "List[_2889.AnalysisCaseVariable]":
        """List[mastapy.system_model.analyses_and_results.AnalysisCaseVariable]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricStudyLoggingVariables")

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
    def edit_folder_path(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "EditFolderPath")

    @exception_bridge
    @enforce_parameter_types
    def add_logging_variable(
        self: "Self", design_entity: "_2414.DesignEntity", path: "List[str]"
    ) -> "_2889.AnalysisCaseVariable":
        """mastapy.system_model.analyses_and_results.AnalysisCaseVariable

        Args:
            design_entity (mastapy.system_model.DesignEntity)
            path (List[str])
        """
        path = conversion.mp_to_pn_list_string(path)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddLoggingVariable",
            design_entity.wrapped if design_entity else None,
            path,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_study_variable(
        self: "Self", design_entity: "_2414.DesignEntity", path: "List[str]"
    ) -> "_4660.ParametricStudyVariable":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable

        Args:
            design_entity (mastapy.system_model.DesignEntity)
            path (List[str])
        """
        path = conversion.mp_to_pn_list_string(path)
        method_result = pythonnet_method_call(
            self.wrapped,
            "AddStudyVariable",
            design_entity.wrapped if design_entity else None,
            path,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def data_logger_for(
        self: "Self", design_entity: "_2414.DesignEntity"
    ) -> "_1760.DataLogger":
        """mastapy.math_utility.convergence.DataLogger

        Args:
            design_entity (mastapy.system_model.DesignEntity)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "DataLoggerFor",
            design_entity.wrapped if design_entity else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def move_study_variable_down(
        self: "Self", study_variable: "_4660.ParametricStudyVariable"
    ) -> None:
        """Method does not return.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """
        pythonnet_method_call(
            self.wrapped,
            "MoveStudyVariableDown",
            study_variable.wrapped if study_variable else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def move_study_variable_up(
        self: "Self", study_variable: "_4660.ParametricStudyVariable"
    ) -> None:
        """Method does not return.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """
        pythonnet_method_call(
            self.wrapped,
            "MoveStudyVariableUp",
            study_variable.wrapped if study_variable else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_logging_variable(
        self: "Self", analysis_variable: "_2889.AnalysisCaseVariable"
    ) -> None:
        """Method does not return.

        Args:
            analysis_variable (mastapy.system_model.analyses_and_results.AnalysisCaseVariable)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveLoggingVariable",
            analysis_variable.wrapped if analysis_variable else None,
        )

    @exception_bridge
    @enforce_parameter_types
    def remove_study_variable(
        self: "Self", study_variable: "_4660.ParametricStudyVariable"
    ) -> None:
        """Method does not return.

        Args:
            study_variable (mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyVariable)
        """
        pythonnet_method_call(
            self.wrapped,
            "RemoveStudyVariable",
            study_variable.wrapped if study_variable else None,
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
    def cast_to(self: "Self") -> "_Cast_ParametricStudyToolOptions":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyToolOptions
        """
        return _Cast_ParametricStudyToolOptions(self)
