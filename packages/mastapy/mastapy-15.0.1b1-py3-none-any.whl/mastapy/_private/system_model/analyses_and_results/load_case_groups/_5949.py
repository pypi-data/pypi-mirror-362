"""AbstractLoadCaseGroup"""

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

_ABSTRACT_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups",
    "AbstractLoadCaseGroup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model import _2411
    from mastapy._private.system_model.analyses_and_results.load_case_groups import (
        _5948,
        _5950,
        _5953,
        _5954,
        _5957,
        _5961,
    )
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4656,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7673,
        _7819,
    )

    Self = TypeVar("Self", bound="AbstractLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="AbstractLoadCaseGroup._Cast_AbstractLoadCaseGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractLoadCaseGroup:
    """Special nested class for casting AbstractLoadCaseGroup to subclasses."""

    __parent__: "AbstractLoadCaseGroup"

    @property
    def abstract_design_state_load_case_group(
        self: "CastSelf",
    ) -> "_5948.AbstractDesignStateLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5948,
        )

        return self.__parent__._cast(_5948.AbstractDesignStateLoadCaseGroup)

    @property
    def abstract_static_load_case_group(
        self: "CastSelf",
    ) -> "_5950.AbstractStaticLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5950,
        )

        return self.__parent__._cast(_5950.AbstractStaticLoadCaseGroup)

    @property
    def design_state(self: "CastSelf") -> "_5953.DesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5953,
        )

        return self.__parent__._cast(_5953.DesignState)

    @property
    def duty_cycle(self: "CastSelf") -> "_5954.DutyCycle":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5954,
        )

        return self.__parent__._cast(_5954.DutyCycle)

    @property
    def sub_group_in_single_design_state(
        self: "CastSelf",
    ) -> "_5957.SubGroupInSingleDesignState":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5957,
        )

        return self.__parent__._cast(_5957.SubGroupInSingleDesignState)

    @property
    def time_series_load_case_group(
        self: "CastSelf",
    ) -> "_5961.TimeSeriesLoadCaseGroup":
        from mastapy._private.system_model.analyses_and_results.load_case_groups import (
            _5961,
        )

        return self.__parent__._cast(_5961.TimeSeriesLoadCaseGroup)

    @property
    def abstract_load_case_group(self: "CastSelf") -> "AbstractLoadCaseGroup":
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
class AbstractLoadCaseGroup(_0.APIBase):
    """AbstractLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_LOAD_CASE_GROUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def number_of_load_cases(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfLoadCases")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_duration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TotalDuration")

        if temp is None:
            return 0.0

        return temp

    @total_duration.setter
    @exception_bridge
    @enforce_parameter_types
    def total_duration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TotalDuration", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def model(self: "Self") -> "_2411.Design":
        """mastapy.system_model.Design

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parametric_analysis_options(self: "Self") -> "_4656.ParametricStudyToolOptions":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.ParametricStudyToolOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParametricAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_case_root_assemblies(self: "Self") -> "List[_7819.RootAssemblyLoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseRootAssemblies")

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
    @enforce_parameter_types
    def create_load_cases(
        self: "Self", number_of_load_cases: "int", token: "_7901.TaskProgress"
    ) -> "List[_7673.LoadCase]":
        """List[mastapy.system_model.analyses_and_results.static_loads.LoadCase]

        Args:
            number_of_load_cases (int)
            token (mastapy.TaskProgress)
        """
        number_of_load_cases = int(number_of_load_cases)
        return conversion.pn_to_mp_objects_in_list(
            pythonnet_method_call(
                self.wrapped,
                "CreateLoadCases",
                number_of_load_cases if number_of_load_cases else 0,
                token.wrapped if token else None,
            )
        )

    @exception_bridge
    def perform_pst(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "PerformPst")

    @exception_bridge
    @enforce_parameter_types
    def perform_pst_with_progress(self: "Self", progress: "_7901.TaskProgress") -> None:
        """Method does not return.

        Args:
            progress (mastapy.TaskProgress)
        """
        pythonnet_method_call(
            self.wrapped,
            "PerformPstWithProgress",
            progress.wrapped if progress else None,
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
    def cast_to(self: "Self") -> "_Cast_AbstractLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_AbstractLoadCaseGroup
        """
        return _Cast_AbstractLoadCaseGroup(self)
