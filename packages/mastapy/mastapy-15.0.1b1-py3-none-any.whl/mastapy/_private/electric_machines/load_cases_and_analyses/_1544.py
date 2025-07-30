"""ElectricMachineLoadCaseGroup"""

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

_ELECTRIC_MACHINE_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "ElectricMachineLoadCaseGroup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines import _1394
    from mastapy._private.electric_machines.load_cases_and_analyses import (
        _1530,
        _1532,
        _1535,
        _1542,
        _1543,
        _1545,
        _1548,
        _1559,
        _1560,
    )
    from mastapy._private.utility import _1782

    Self = TypeVar("Self", bound="ElectricMachineLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineLoadCaseGroup._Cast_ElectricMachineLoadCaseGroup",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ElectricMachineLoadCaseGroup:
    """Special nested class for casting ElectricMachineLoadCaseGroup to subclasses."""

    __parent__: "ElectricMachineLoadCaseGroup"

    @property
    def electric_machine_load_case_group(
        self: "CastSelf",
    ) -> "ElectricMachineLoadCaseGroup":
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
class ElectricMachineLoadCaseGroup(_0.APIBase):
    """ElectricMachineLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ELECTRIC_MACHINE_LOAD_CASE_GROUP

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
    def dynamic_forces_load_cases(self: "Self") -> "List[_1532.DynamicForceLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.DynamicForceLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicForcesLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def dynamic_forces_load_cases_without_non_linear_dq_model(
        self: "Self",
    ) -> "List[_1530.BasicDynamicForceLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.BasicDynamicForceLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicForcesLoadCasesWithoutNonLinearDQModel"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def efficiency_map_load_cases(self: "Self") -> "List[_1535.EfficiencyMapLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.EfficiencyMapLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EfficiencyMapLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mechanical_load_cases(
        self: "Self",
    ) -> "List[_1545.ElectricMachineMechanicalLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.ElectricMachineMechanicalLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MechanicalLoadCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def single_operating_point_load_cases_with_non_linear_dq_model(
        self: "Self",
    ) -> "List[_1560.SpeedTorqueLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.SpeedTorqueLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SingleOperatingPointLoadCasesWithNonLinearDQModel"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def single_operating_point_load_cases_without_non_linear_dq_model(
        self: "Self",
    ) -> "List[_1542.ElectricMachineLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SingleOperatingPointLoadCasesWithoutNonLinearDQModel"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def speed_torque_curve_load_cases(
        self: "Self",
    ) -> "List[_1559.SpeedTorqueCurveLoadCase]":
        """List[mastapy.electric_machines.load_cases_and_analyses.SpeedTorqueCurveLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedTorqueCurveLoadCases")

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
    def add_load_case(
        self: "Self", load_case_type: "_1548.LoadCaseType"
    ) -> "_1543.ElectricMachineLoadCaseBase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase

        Args:
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        method_result = pythonnet_method_call(
            self.wrapped, "AddLoadCase", load_case_type
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def add_load_case_named(
        self: "Self", load_case_type: "_1548.LoadCaseType", name: "str"
    ) -> "_1543.ElectricMachineLoadCaseBase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase

        Args:
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
            name (str)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddLoadCaseNamed", load_case_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def load_case_named(
        self: "Self", load_case_type: "_1548.LoadCaseType", name: "str"
    ) -> "_1543.ElectricMachineLoadCaseBase":
        """mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase

        Args:
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
            name (str)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "LoadCaseNamed", load_case_type, name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_compound_analysis(
        self: "Self",
        setup: "_1394.ElectricMachineSetup",
        load_case_type: "_1548.LoadCaseType",
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "PerformCompoundAnalysis",
            setup.wrapped if setup else None,
            load_case_type,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def perform_compound_analysis_with_progress(
        self: "Self",
        setup: "_1394.ElectricMachineSetup",
        load_case_type: "_1548.LoadCaseType",
        task_progress: "_7901.TaskProgress",
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            setup (mastapy.electric_machines.ElectricMachineSetup)
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
            task_progress (mastapy.TaskProgress)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        method_result = pythonnet_method_call(
            self.wrapped,
            "PerformCompoundAnalysisWithProgress",
            setup.wrapped if setup else None,
            load_case_type,
            task_progress.wrapped if task_progress else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def remove_all_electric_machine_load_cases(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "RemoveAllElectricMachineLoadCases")

    @exception_bridge
    @enforce_parameter_types
    def try_remove_load_case(
        self: "Self", load_case: "_1543.ElectricMachineLoadCaseBase"
    ) -> "bool":
        """bool

        Args:
            load_case (mastapy.electric_machines.load_cases_and_analyses.ElectricMachineLoadCaseBase)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "TryRemoveLoadCase", load_case.wrapped if load_case else None
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def try_remove_load_case_named(
        self: "Self", load_case_type: "_1548.LoadCaseType", name: "str"
    ) -> "bool":
        """bool

        Args:
            load_case_type (mastapy.electric_machines.load_cases_and_analyses.LoadCaseType)
            name (str)
        """
        load_case_type = conversion.mp_to_pn_enum(
            load_case_type,
            "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses.LoadCaseType",
        )
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "TryRemoveLoadCaseNamed", load_case_type, name if name else ""
        )
        return method_result

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
    def cast_to(self: "Self") -> "_Cast_ElectricMachineLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_ElectricMachineLoadCaseGroup
        """
        return _Cast_ElectricMachineLoadCaseGroup(self)
