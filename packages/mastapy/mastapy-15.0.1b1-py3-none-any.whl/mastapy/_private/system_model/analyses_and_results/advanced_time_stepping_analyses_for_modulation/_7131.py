"""AdvancedTimeSteppingAnalysisForModulationOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import list_with_selected_item
from mastapy._private._internal.list_with_selected_item import (
    promote_to_list_with_selected_item,
)
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.sentinels import ListWithSelectedItem_None
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "AdvancedTimeSteppingAnalysisForModulationOptions",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2925
    from mastapy._private.system_model.analyses_and_results.static_loads import (
        _7681,
        _7764,
    )

    Self = TypeVar("Self", bound="AdvancedTimeSteppingAnalysisForModulationOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedTimeSteppingAnalysisForModulationOptions._Cast_AdvancedTimeSteppingAnalysisForModulationOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedTimeSteppingAnalysisForModulationOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AdvancedTimeSteppingAnalysisForModulationOptions:
    """Special nested class for casting AdvancedTimeSteppingAnalysisForModulationOptions to subclasses."""

    __parent__: "AdvancedTimeSteppingAnalysisForModulationOptions"

    @property
    def advanced_time_stepping_analysis_for_modulation_options(
        self: "CastSelf",
    ) -> "AdvancedTimeSteppingAnalysisForModulationOptions":
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
class AdvancedTimeSteppingAnalysisForModulationOptions(_0.APIBase):
    """AdvancedTimeSteppingAnalysisForModulationOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def advanced_time_stepping_analysis_method(
        self: "Self",
    ) -> "_7681.AdvancedTimeSteppingAnalysisForModulationType":
        """mastapy.system_model.analyses_and_results.static_loads.AdvancedTimeSteppingAnalysisForModulationType"""
        temp = pythonnet_property_get(
            self.wrapped, "AdvancedTimeSteppingAnalysisMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.AdvancedTimeSteppingAnalysisForModulationType",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.analyses_and_results.static_loads._7681",
            "AdvancedTimeSteppingAnalysisForModulationType",
        )(value)

    @advanced_time_stepping_analysis_method.setter
    @exception_bridge
    @enforce_parameter_types
    def advanced_time_stepping_analysis_method(
        self: "Self", value: "_7681.AdvancedTimeSteppingAnalysisForModulationType"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads.AdvancedTimeSteppingAnalysisForModulationType",
        )
        pythonnet_property_set(
            self.wrapped, "AdvancedTimeSteppingAnalysisMethod", value
        )

    @property
    @exception_bridge
    def allow_bearing_element_orbit_for_quasi_steps(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped, "AllowBearingElementOrbitForQuasiSteps"
        )

        if temp is None:
            return False

        return temp

    @allow_bearing_element_orbit_for_quasi_steps.setter
    @exception_bridge
    @enforce_parameter_types
    def allow_bearing_element_orbit_for_quasi_steps(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowBearingElementOrbitForQuasiSteps",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def include_time_offset_for_steady_state(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeTimeOffsetForSteadyState")

        if temp is None:
            return False

        return temp

    @include_time_offset_for_steady_state.setter
    @exception_bridge
    @enforce_parameter_types
    def include_time_offset_for_steady_state(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeTimeOffsetForSteadyState",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts(
        self: "Self",
    ) -> "list_with_selected_item.ListWithSelectedItem_StaticLoadCase":
        """ListWithSelectedItem[mastapy.system_model.analyses_and_results.static_loads.StaticLoadCase]"""
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptionsAndActiveFEParts",
        )

        if temp is None:
            return None

        selected_value = temp.SelectedValue

        if selected_value is None:
            return ListWithSelectedItem_None(temp)

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.list_with_selected_item",
            "ListWithSelectedItem_StaticLoadCase",
        )(temp)

    @load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts(
        self: "Self", value: "_7674.StaticLoadCase"
    ) -> None:
        generic_type = (
            list_with_selected_item.ListWithSelectedItem_StaticLoadCase.implicit_type()
        )
        value = promote_to_list_with_selected_item(value)
        value = conversion.mp_to_pn_smt_list_with_selected_item(
            self, value, generic_type
        )
        pythonnet_property_set(
            self.wrapped,
            "LoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptionsAndActiveFEParts",
            value,
        )

    @property
    @exception_bridge
    def number_of_periods_for_advanced_time_stepping_analysis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfPeriodsForAdvancedTimeSteppingAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @number_of_periods_for_advanced_time_stepping_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_periods_for_advanced_time_stepping_analysis(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfPeriodsForAdvancedTimeSteppingAnalysis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_steps_for_advanced_time_stepping_analysis(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfStepsForAdvancedTimeSteppingAnalysis"
        )

        if temp is None:
            return 0

        return temp

    @number_of_steps_for_advanced_time_stepping_analysis.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_steps_for_advanced_time_stepping_analysis(
        self: "Self", value: "int"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfStepsForAdvancedTimeSteppingAnalysis",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def number_of_times_per_quasi_step(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTimesPerQuasiStep")

        if temp is None:
            return 0

        return temp

    @number_of_times_per_quasi_step.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_times_per_quasi_step(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTimesPerQuasiStep",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def tolerance_for_compatibility_of_atsam_and_te_periods_check(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ToleranceForCompatibilityOfATSAMAndTEPeriodsCheck"
        )

        if temp is None:
            return 0.0

        return temp

    @tolerance_for_compatibility_of_atsam_and_te_periods_check.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance_for_compatibility_of_atsam_and_te_periods_check(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ToleranceForCompatibilityOfATSAMAndTEPeriodsCheck",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def use_this_load_case_for_load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts(
        self: "Self",
    ) -> "bool":
        """bool"""
        temp = pythonnet_property_get(
            self.wrapped,
            "UseThisLoadCaseForLoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptionsAndActiveFEParts",
        )

        if temp is None:
            return False

        return temp

    @use_this_load_case_for_load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def use_this_load_case_for_load_case_for_advanced_time_stepping_analysis_for_modulation_time_options_and_active_fe_parts(
        self: "Self", value: "bool"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseThisLoadCaseForLoadCaseForAdvancedTimeSteppingAnalysisForModulationTimeOptionsAndActiveFEParts",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def gear_set_load_case_within_load_case_for_advanced_time_stepping_analysis_for_modulation(
        self: "Self",
    ) -> "_7764.GearSetLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "GearSetLoadCaseWithinLoadCaseForAdvancedTimeSteppingAnalysisForModulation",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def time_options(self: "Self") -> "_2925.TimeOptions":
        """mastapy.system_model.analyses_and_results.TimeOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AdvancedTimeSteppingAnalysisForModulationOptions":
        """Cast to another type.

        Returns:
            _Cast_AdvancedTimeSteppingAnalysisForModulationOptions
        """
        return _Cast_AdvancedTimeSteppingAnalysisForModulationOptions(self)
