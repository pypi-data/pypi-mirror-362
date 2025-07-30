"""ModalAnalysisBarModelBaseFEExportOptions"""

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
from mastapy._private.nodal_analysis import _56
from mastapy._private.nodal_analysis.fe_export_utility import _246
from mastapy._private.system_model.part_model import _2680
from mastapy._private.utility.units_and_measurements import _1802

_MODAL_ANALYSIS_BAR_MODEL_BASE_FE_EXPORT_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "ModalAnalysisBarModelBaseFEExportOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.nodal_analysis import _55
    from mastapy._private.nodal_analysis.dev_tools_analyses import _263
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6053,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4928

    Self = TypeVar("Self", bound="ModalAnalysisBarModelBaseFEExportOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalAnalysisBarModelBaseFEExportOptions._Cast_ModalAnalysisBarModelBaseFEExportOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalAnalysisBarModelBaseFEExportOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModalAnalysisBarModelBaseFEExportOptions:
    """Special nested class for casting ModalAnalysisBarModelBaseFEExportOptions to subclasses."""

    __parent__: "ModalAnalysisBarModelBaseFEExportOptions"

    @property
    def modal_analysis_bar_model_fe_export_options(
        self: "CastSelf",
    ) -> "_4928.ModalAnalysisBarModelFEExportOptions":
        from mastapy._private.system_model.analyses_and_results.modal_analyses import (
            _4928,
        )

        return self.__parent__._cast(_4928.ModalAnalysisBarModelFEExportOptions)

    @property
    def harmonic_analysis_bar_model_fe_export_options(
        self: "CastSelf",
    ) -> "_6053.HarmonicAnalysisBarModelFEExportOptions":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
            _6053,
        )

        return self.__parent__._cast(_6053.HarmonicAnalysisBarModelFEExportOptions)

    @property
    def modal_analysis_bar_model_base_fe_export_options(
        self: "CastSelf",
    ) -> "ModalAnalysisBarModelBaseFEExportOptions":
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
class ModalAnalysisBarModelBaseFEExportOptions(_0.APIBase):
    """ModalAnalysisBarModelBaseFEExportOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODAL_ANALYSIS_BAR_MODEL_BASE_FE_EXPORT_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_type(self: "Self") -> "_55.BarModelAnalysisType":
        """mastapy.nodal_analysis.BarModelAnalysisType"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.BarModelAnalysisType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._55", "BarModelAnalysisType"
        )(value)

    @analysis_type.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_type(self: "Self", value: "_55.BarModelAnalysisType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.NodalAnalysis.BarModelAnalysisType"
        )
        pythonnet_property_set(self.wrapped, "AnalysisType", value)

    @property
    @exception_bridge
    def connect_to_full_fe_mesh(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ConnectToFullFEMesh")

        if temp is None:
            return False

        return temp

    @connect_to_full_fe_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def connect_to_full_fe_mesh(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConnectToFullFEMesh",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def coordinate_system(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_FEPart":
        """ListWithSelectedItem[mastapy.system_model.part_model.FEPart]"""
        temp = pythonnet_property_get(self.wrapped, "CoordinateSystem")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FEPart",
        )(temp)

    @coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def coordinate_system(self: "Self", value: "_2680.FEPart") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "CoordinateSystem", value)

    @property
    @exception_bridge
    def error_message(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ErrorMessage")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def fe_file_to_include(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FEFileToInclude")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def fe_package(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FEExportFormat":
        """EnumWithSelectedValue[mastapy.nodal_analysis.fe_export_utility.FEExportFormat]"""
        temp = pythonnet_property_get(self.wrapped, "FEPackage")

        if temp is None:
            return None

        value = (
            enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.wrapped_type()
        )
        return enum_with_selected_value_runtime.create(temp, value)

    @fe_package.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_package(self: "Self", value: "_246.FEExportFormat") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FEExportFormat.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FEPackage", value)

    @property
    @exception_bridge
    def fe_part(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_FEPart":
        """ListWithSelectedItem[mastapy.system_model.part_model.FEPart]"""
        temp = pythonnet_property_get(self.wrapped, "FEPart")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_FEPart",
        )(temp)

    @fe_part.setter
    @exception_bridge
    @enforce_parameter_types
    def fe_part(self: "Self", value: "_2680.FEPart") -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_FEPart.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "FEPart", value)

    @property
    @exception_bridge
    def force_unit(self: "Self") -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "ForceUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @force_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def force_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "ForceUnit", value)

    @property
    @exception_bridge
    def length_unit(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_Unit":
        """ListWithSelectedItem[mastapy.utility.units_and_measurements.Unit]"""
        temp = pythonnet_property_get(self.wrapped, "LengthUnit")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_Unit",
        )(temp)

    @length_unit.setter
    @exception_bridge
    @enforce_parameter_types
    def length_unit(self: "Self", value: "_1802.Unit") -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_Unit.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "LengthUnit", value)

    @property
    @exception_bridge
    def shaft_export_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BarModelExportType":
        """EnumWithSelectedValue[mastapy.nodal_analysis.BarModelExportType]"""
        temp = pythonnet_property_get(self.wrapped, "ShaftExportType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BarModelExportType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @shaft_export_type.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_export_type(self: "Self", value: "_56.BarModelExportType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BarModelExportType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ShaftExportType", value)

    @property
    @exception_bridge
    def use_fe_file_from_fe_substructure(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseFEFileFromFESubstructure")

        if temp is None:
            return False

        return temp

    @use_fe_file_from_fe_substructure.setter
    @exception_bridge
    @enforce_parameter_types
    def use_fe_file_from_fe_substructure(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseFEFileFromFESubstructure",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mode_options(self: "Self") -> "_263.EigenvalueOptions":
        """mastapy.nodal_analysis.dev_tools_analyses.EigenvalueOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModeOptions")

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
    def export_to_file(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "ExportToFile", file_path)

    @exception_bridge
    @enforce_parameter_types
    def set_fe_file_to_include(
        self: "Self",
        file_path: "PathLike",
        format_: "_246.FEExportFormat",
        length_scale: "float" = 1.0,
        force_scale: "float" = 1.0,
    ) -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
            format_ (mastapy.nodal_analysis.fe_export_utility.FEExportFormat)
            length_scale (float, optional)
            force_scale (float, optional)
        """
        file_path = str(file_path)
        format_ = conversion.mp_to_pn_enum(
            format_, "SMT.MastaAPI.NodalAnalysis.FeExportUtility.FEExportFormat"
        )
        length_scale = float(length_scale)
        force_scale = float(force_scale)
        pythonnet_method_call(
            self.wrapped,
            "SetFEFileToInclude",
            file_path,
            format_,
            length_scale if length_scale else 0.0,
            force_scale if force_scale else 0.0,
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
    def cast_to(self: "Self") -> "_Cast_ModalAnalysisBarModelBaseFEExportOptions":
        """Cast to another type.

        Returns:
            _Cast_ModalAnalysisBarModelBaseFEExportOptions
        """
        return _Cast_ModalAnalysisBarModelBaseFEExportOptions(self)
