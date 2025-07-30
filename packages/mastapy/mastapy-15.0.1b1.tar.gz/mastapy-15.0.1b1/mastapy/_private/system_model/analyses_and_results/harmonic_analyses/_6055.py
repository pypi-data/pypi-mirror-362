"""HarmonicAnalysisExportOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

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
)
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6036
from mastapy._private.system_model.analyses_and_results.modal_analyses import _4897
from mastapy._private.utility.units_and_measurements import _1802

_HARMONIC_ANALYSIS_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6056,
        _6058,
        _6059,
        _6060,
        _6061,
    )
    from mastapy._private.system_model.part_model import _2698

    Self = TypeVar("Self", bound="HarmonicAnalysisExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisExportOptions._Cast_HarmonicAnalysisExportOptions",
    )

TPartAnalysis = TypeVar("TPartAnalysis")
TPart = TypeVar("TPart", bound="_2698.Part")

__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisExportOptions:
    """Special nested class for casting HarmonicAnalysisExportOptions to subclasses."""

    __parent__: "HarmonicAnalysisExportOptions"

    @property
    def harmonic_analysis_fe_export_options(
        self: "CastSelf",
    ) -> "_6056.HarmonicAnalysisFEExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6056,
        )

        return self.__parent__._cast(_6056.HarmonicAnalysisFEExportOptions)

    @property
    def harmonic_analysis_root_assembly_and_fe_shared_export_options(
        self: "CastSelf",
    ) -> "_6059.HarmonicAnalysisRootAssemblyAndFESharedExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6059,
        )

        return self.__parent__._cast(
            _6059.HarmonicAnalysisRootAssemblyAndFESharedExportOptions
        )

    @property
    def harmonic_analysis_root_assembly_export_options(
        self: "CastSelf",
    ) -> "_6060.HarmonicAnalysisRootAssemblyExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6060,
        )

        return self.__parent__._cast(_6060.HarmonicAnalysisRootAssemblyExportOptions)

    @property
    def harmonic_analysis_shaft_export_options(
        self: "CastSelf",
    ) -> "_6061.HarmonicAnalysisShaftExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6061,
        )

        return self.__parent__._cast(_6061.HarmonicAnalysisShaftExportOptions)

    @property
    def harmonic_analysis_export_options(
        self: "CastSelf",
    ) -> "HarmonicAnalysisExportOptions":
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
class HarmonicAnalysisExportOptions(_0.APIBase, Generic[TPartAnalysis, TPart]):
    """HarmonicAnalysisExportOptions

    This is a mastapy class.

    Generic Types:
        TPartAnalysis
        TPart
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_units_for_export(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceUnitsForExport")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @distance_units_for_export.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_units_for_export(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "DistanceUnitsForExport", value)

    @property
    @exception_bridge
    def export_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ExportOutputType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.ExportOutputType]"""
        temp = pythonnet_property_get(self.wrapped, "ExportType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ExportOutputType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @export_type.setter
    @exception_bridge
    @enforce_parameter_types
    def export_type(self: "Self", value: "_6036.ExportOutputType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ExportOutputType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ExportType", value)

    @property
    @exception_bridge
    def planetary_duplicate_to_export(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_TPartAnalysis":
        """ListWithSelectedItem[TPartAnalysis]"""
        temp = pythonnet_property_get(self.wrapped, "PlanetaryDuplicateToExport")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_TPartAnalysis",
        )(temp)

    @planetary_duplicate_to_export.setter
    @exception_bridge
    @enforce_parameter_types
    def planetary_duplicate_to_export(self: "Self", value: "TPartAnalysis") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_TPartAnalysis.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "PlanetaryDuplicateToExport", value)

    @property
    @exception_bridge
    def status_message_for_export(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StatusMessageForExport")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def type_of_result_to_export(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.modal_analyses.DynamicsResponseType]"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfResultToExport")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @type_of_result_to_export.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_result_to_export(
        self: "Self", value: "_4897.DynamicsResponseType"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DynamicsResponseType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TypeOfResultToExport", value)

    @property
    @exception_bridge
    def analysis_options(self: "Self") -> "_6058.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisOptions")

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
    def export_results(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ExportResults")

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
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisExportOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisExportOptions
        """
        return _Cast_HarmonicAnalysisExportOptions(self)
