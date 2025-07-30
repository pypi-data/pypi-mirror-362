"""DutyCycleResultsForAllComponents"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DUTY_CYCLE_RESULTS_FOR_ALL_COMPONENTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "DutyCycleResultsForAllComponents",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.parametric_study_tools import (
        _4616,
        _4617,
        _4618,
        _4619,
    )

    Self = TypeVar("Self", bound="DutyCycleResultsForAllComponents")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DutyCycleResultsForAllComponents._Cast_DutyCycleResultsForAllComponents",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DutyCycleResultsForAllComponents",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_DutyCycleResultsForAllComponents:
    """Special nested class for casting DutyCycleResultsForAllComponents to subclasses."""

    __parent__: "DutyCycleResultsForAllComponents"

    @property
    def duty_cycle_results_for_all_components(
        self: "CastSelf",
    ) -> "DutyCycleResultsForAllComponents":
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
class DutyCycleResultsForAllComponents(_0.APIBase):
    """DutyCycleResultsForAllComponents

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _DUTY_CYCLE_RESULTS_FOR_ALL_COMPONENTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def results_for_all_gear_sets(
        self: "Self",
    ) -> "_4616.DutyCycleResultsForAllGearSets":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DutyCycleResultsForAllGearSets

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForAllGearSets")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def results_for_root_assembly(
        self: "Self",
    ) -> "_4617.DutyCycleResultsForRootAssembly":
        """mastapy.system_model.analyses_and_results.parametric_study_tools.DutyCycleResultsForRootAssembly

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForRootAssembly")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def results_for_all_bearings(
        self: "Self",
    ) -> "List[_4618.DutyCycleResultsForSingleBearing]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.DutyCycleResultsForSingleBearing]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForAllBearings")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def results_for_all_shafts(
        self: "Self",
    ) -> "List[_4619.DutyCycleResultsForSingleShaft]":
        """List[mastapy.system_model.analyses_and_results.parametric_study_tools.DutyCycleResultsForSingleShaft]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultsForAllShafts")

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
    def cast_to(self: "Self") -> "_Cast_DutyCycleResultsForAllComponents":
        """Cast to another type.

        Returns:
            _Cast_DutyCycleResultsForAllComponents
        """
        return _Cast_DutyCycleResultsForAllComponents(self)
