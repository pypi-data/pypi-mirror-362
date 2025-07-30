"""HarmonicAnalysisOptions"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
    _6021,
    _6081,
)
from mastapy._private.system_model.part_model.acoustics import _2867

_HARMONIC_ANALYSIS_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisOptions",
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1718
    from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
        _7191,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6043,
        _6095,
        _6107,
        _6114,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.results import (
        _6153,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses import (
        _6148,
    )
    from mastapy._private.system_model.analyses_and_results.modal_analyses import _4930

    Self = TypeVar("Self", bound="HarmonicAnalysisOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicAnalysisOptions._Cast_HarmonicAnalysisOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisOptions:
    """Special nested class for casting HarmonicAnalysisOptions to subclasses."""

    __parent__: "HarmonicAnalysisOptions"

    @property
    def harmonic_analysis_options_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "_7191.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation":
        from mastapy._private.system_model.analyses_and_results.advanced_time_stepping_analyses_for_modulation import (
            _7191,
        )

        return self.__parent__._cast(
            _7191.HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation
        )

    @property
    def harmonic_analysis_options(self: "CastSelf") -> "HarmonicAnalysisOptions":
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
class HarmonicAnalysisOptions(_0.APIBase):
    """HarmonicAnalysisOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def acoustic_analysis_setup(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_AcousticAnalysisSetup":
        """ListWithSelectedItem[mastapy.system_model.part_model.acoustics.AcousticAnalysisSetup]"""
        temp = pythonnet_property_get(self.wrapped, "AcousticAnalysisSetup")

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_AcousticAnalysisSetup",
        )(temp)

    @acoustic_analysis_setup.setter
    @exception_bridge
    @enforce_parameter_types
    def acoustic_analysis_setup(
        self: "Self", value: "_2867.AcousticAnalysisSetup"
    ) -> None:
        generic_type = list_with_selected_item.ListWithSelectedItem_AcousticAnalysisSetup.implicit_type()
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(self.wrapped, "AcousticAnalysisSetup", value)

    @property
    @exception_bridge
    def amplitude_cut_off_for_linear_te(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AmplitudeCutOffForLinearTE")

        if temp is None:
            return 0.0

        return temp

    @amplitude_cut_off_for_linear_te.setter
    @exception_bridge
    @enforce_parameter_types
    def amplitude_cut_off_for_linear_te(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AmplitudeCutOffForLinearTE",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def amplitude_cut_off_for_misalignment_excitation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AmplitudeCutOffForMisalignmentExcitation"
        )

        if temp is None:
            return 0.0

        return temp

    @amplitude_cut_off_for_misalignment_excitation.setter
    @exception_bridge
    @enforce_parameter_types
    def amplitude_cut_off_for_misalignment_excitation(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AmplitudeCutOffForMisalignmentExcitation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def calculate_uncoupled_modes_during_analysis(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CalculateUncoupledModesDuringAnalysis"
        )

        if temp is None:
            return False

        return temp

    @calculate_uncoupled_modes_during_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def calculate_uncoupled_modes_during_analysis(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CalculateUncoupledModesDuringAnalysis",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def constant_modal_damping(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ConstantModalDamping")

        if temp is None:
            return 0.0

        return temp

    @constant_modal_damping.setter
    @exception_bridge
    @enforce_parameter_types
    def constant_modal_damping(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ConstantModalDamping",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def crop_to_speed_range_for_export_and_reports(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "CropToSpeedRangeForExportAndReports"
        )

        if temp is None:
            return False

        return temp

    @crop_to_speed_range_for_export_and_reports.setter
    @exception_bridge
    @enforce_parameter_types
    def crop_to_speed_range_for_export_and_reports(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CropToSpeedRangeForExportAndReports",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def damping_specification(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_DampingSpecification":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.DampingSpecification]"""
        temp = pythonnet_property_get(self.wrapped, "DampingSpecification")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_DampingSpecification.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @damping_specification.setter
    @exception_bridge
    @enforce_parameter_types
    def damping_specification(
        self: "Self", value: "_6021.DampingSpecification"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_DampingSpecification.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "DampingSpecification", value)

    @property
    @exception_bridge
    def modal_correction_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ModalCorrectionMethod":
        """EnumWithSelectedValue[mastapy.system_model.analyses_and_results.harmonic_analyses.ModalCorrectionMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ModalCorrectionMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ModalCorrectionMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @modal_correction_method.setter
    @exception_bridge
    @enforce_parameter_types
    def modal_correction_method(
        self: "Self", value: "_6081.ModalCorrectionMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ModalCorrectionMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ModalCorrectionMethod", value)

    @property
    @exception_bridge
    def number_of_harmonics(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfHarmonics")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_harmonics.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_harmonics(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfHarmonics", value)

    @property
    @exception_bridge
    def per_frequency_damping_profile(self: "Self") -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(self.wrapped, "PerFrequencyDampingProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @per_frequency_damping_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def per_frequency_damping_profile(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "PerFrequencyDampingProfile", value.wrapped
        )

    @property
    @exception_bridge
    def rayleigh_damping_alpha(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingAlpha")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_alpha.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_alpha(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingAlpha",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rayleigh_damping_beta(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RayleighDampingBeta")

        if temp is None:
            return 0.0

        return temp

    @rayleigh_damping_beta.setter
    @exception_bridge
    @enforce_parameter_types
    def rayleigh_damping_beta(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RayleighDampingBeta",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def response_cache_level(self: "Self") -> "_6095.ResponseCacheLevel":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.ResponseCacheLevel"""
        temp = pythonnet_property_get(self.wrapped, "ResponseCacheLevel")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ResponseCacheLevel",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.harmonic_analyses._6095",
            "ResponseCacheLevel",
        )(value)

    @response_cache_level.setter
    @exception_bridge
    @enforce_parameter_types
    def response_cache_level(self: "Self", value: "_6095.ResponseCacheLevel") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ResponseCacheLevel",
        )
        pythonnet_property_set(self.wrapped, "ResponseCacheLevel", value)

    @property
    @exception_bridge
    def update_dynamic_response_chart_on_change_of_settings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "UpdateDynamicResponseChartOnChangeOfSettings"
        )

        if temp is None:
            return False

        return temp

    @update_dynamic_response_chart_on_change_of_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def update_dynamic_response_chart_on_change_of_settings(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UpdateDynamicResponseChartOnChangeOfSettings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_linear_extrapolation(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseLinearExtrapolation")

        if temp is None:
            return False

        return temp

    @use_linear_extrapolation.setter
    @exception_bridge
    @enforce_parameter_types
    def use_linear_extrapolation(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseLinearExtrapolation",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def excitation_selection(self: "Self") -> "_6153.ExcitationSourceSelectionGroup":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.results.ExcitationSourceSelectionGroup

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExcitationSelection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def frequency_options(
        self: "Self",
    ) -> "_6043.FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrequencyOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def modal_analysis_options(self: "Self") -> "_4930.ModalAnalysisOptions":
        """mastapy.system_model.analyses_and_results.modal_analyses.ModalAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModalAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def reference_speed_options(
        self: "Self",
    ) -> "_6107.SpeedOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.SpeedOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSpeedOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stiffness_options(self: "Self") -> "_6114.StiffnessOptionsForHarmonicAnalysis":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.StiffnessOptionsForHarmonicAnalysis

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StiffnessOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transfer_path_analysis_setup_options(
        self: "Self",
    ) -> "_6148.TransferPathAnalysisSetupOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.transfer_path_analyses.TransferPathAnalysisSetupOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransferPathAnalysisSetupOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def per_mode_damping_factors(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PerModeDampingFactors")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, float)

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
    def set_per_mode_damping_factor(
        self: "Self", mode: "int", damping: "float"
    ) -> None:
        """Method does not return.

        Args:
            mode (int)
            damping (float)
        """
        mode = int(mode)
        damping = float(damping)
        pythonnet_method_call(
            self.wrapped,
            "SetPerModeDampingFactor",
            mode if mode else 0,
            damping if damping else 0.0,
        )

    @exception_bridge
    @enforce_parameter_types
    def set_per_mode_damping_factors(
        self: "Self", damping_values: "List[float]"
    ) -> None:
        """Method does not return.

        Args:
            damping_values (List[float])
        """
        damping_values = conversion.mp_to_pn_list_float(damping_values)
        pythonnet_method_call(self.wrapped, "SetPerModeDampingFactors", damping_values)

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
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisOptions":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisOptions
        """
        return _Cast_HarmonicAnalysisOptions(self)
