"""ThermalLoadCaseGroup"""

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

_THERMAL_LOAD_CASE_GROUP = python_net_import(
    "SMT.MastaAPI.ElectricMachines.Thermal.LoadCasesAndAnalyses", "ThermalLoadCaseGroup"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private import _7901
    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.thermal import _1480, _1481
    from mastapy._private.electric_machines.thermal.load_cases_and_analyses import _1503
    from mastapy._private.utility import _1782

    Self = TypeVar("Self", bound="ThermalLoadCaseGroup")
    CastSelf = TypeVar(
        "CastSelf", bound="ThermalLoadCaseGroup._Cast_ThermalLoadCaseGroup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThermalLoadCaseGroup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ThermalLoadCaseGroup:
    """Special nested class for casting ThermalLoadCaseGroup to subclasses."""

    __parent__: "ThermalLoadCaseGroup"

    @property
    def thermal_load_case_group(self: "CastSelf") -> "ThermalLoadCaseGroup":
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
class ThermalLoadCaseGroup(_0.APIBase):
    """ThermalLoadCaseGroup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _THERMAL_LOAD_CASE_GROUP

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
    def thermal_electric_machine(self: "Self") -> "_1480.ThermalElectricMachine":
        """mastapy.electric_machines.thermal.ThermalElectricMachine

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalElectricMachine")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_cases(self: "Self") -> "List[_1503.ThermalLoadCase]":
        """List[mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCases")

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
        self: "Self", name: "str" = "Load Case"
    ) -> "_1503.ThermalLoadCase":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase

        Args:
            name (str, optional)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "AddLoadCase", name if name else ""
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def load_case_named(self: "Self", name: "str") -> "_1503.ThermalLoadCase":
        """mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "LoadCaseNamed", name if name else ""
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
        self: "Self", setup: "_1481.ThermalElectricMachineSetup"
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            setup (mastapy.electric_machines.thermal.ThermalElectricMachineSetup)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "PerformCompoundAnalysis", setup.wrapped if setup else None
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
        setup: "_1481.ThermalElectricMachineSetup",
        token: "_7901.TaskProgress",
    ) -> "_1782.MethodOutcome":
        """mastapy.utility.MethodOutcome

        Args:
            setup (mastapy.electric_machines.thermal.ThermalElectricMachineSetup)
            token (mastapy.TaskProgress)
        """
        method_result = pythonnet_method_call(
            self.wrapped,
            "PerformCompoundAnalysisWithProgress",
            setup.wrapped if setup else None,
            token.wrapped if token else None,
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    @enforce_parameter_types
    def try_remove_load_case(
        self: "Self", load_case: "_1503.ThermalLoadCase"
    ) -> "bool":
        """bool

        Args:
            load_case (mastapy.electric_machines.thermal.load_cases_and_analyses.ThermalLoadCase)
        """
        method_result = pythonnet_method_call(
            self.wrapped, "TryRemoveLoadCase", load_case.wrapped if load_case else None
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def try_remove_load_case_named(self: "Self", name: "str") -> "bool":
        """bool

        Args:
            name (str)
        """
        name = str(name)
        method_result = pythonnet_method_call(
            self.wrapped, "TryRemoveLoadCaseNamed", name if name else ""
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
    def cast_to(self: "Self") -> "_Cast_ThermalLoadCaseGroup":
        """Cast to another type.

        Returns:
            _Cast_ThermalLoadCaseGroup
        """
        return _Cast_ThermalLoadCaseGroup(self)
