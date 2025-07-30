"""FrequencyOptionsForHarmonicAnalysisResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.analysis_cases import _7878
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_FREQUENCY_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "FrequencyOptionsForHarmonicAnalysisResults",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    Self = TypeVar("Self", bound="FrequencyOptionsForHarmonicAnalysisResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FrequencyOptionsForHarmonicAnalysisResults._Cast_FrequencyOptionsForHarmonicAnalysisResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FrequencyOptionsForHarmonicAnalysisResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FrequencyOptionsForHarmonicAnalysisResults:
    """Special nested class for casting FrequencyOptionsForHarmonicAnalysisResults to subclasses."""

    __parent__: "FrequencyOptionsForHarmonicAnalysisResults"

    @property
    def abstract_analysis_options(self: "CastSelf") -> "_7878.AbstractAnalysisOptions":
        return self.__parent__._cast(_7878.AbstractAnalysisOptions)

    @property
    def frequency_options_for_harmonic_analysis_results(
        self: "CastSelf",
    ) -> "FrequencyOptionsForHarmonicAnalysisResults":
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
class FrequencyOptionsForHarmonicAnalysisResults(
    _7878.AbstractAnalysisOptions[_7674.StaticLoadCase]
):
    """FrequencyOptionsForHarmonicAnalysisResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FREQUENCY_OPTIONS_FOR_HARMONIC_ANALYSIS_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allow_frequencies_greater_than_the_highest_mode(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "AllowFrequenciesGreaterThanTheHighestMode"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @allow_frequencies_greater_than_the_highest_mode.setter
    @exception_bridge
    @enforce_parameter_types
    def allow_frequencies_greater_than_the_highest_mode(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AllowFrequenciesGreaterThanTheHighestMode", value
        )

    @property
    @exception_bridge
    def base_points_on_mode_frequencies(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "BasePointsOnModeFrequencies")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @base_points_on_mode_frequencies.setter
    @exception_bridge
    @enforce_parameter_types
    def base_points_on_mode_frequencies(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "BasePointsOnModeFrequencies", value)

    @property
    @exception_bridge
    def clustering_bias_of_additional_points(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ClusteringBiasOfAdditionalPoints")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @clustering_bias_of_additional_points.setter
    @exception_bridge
    @enforce_parameter_types
    def clustering_bias_of_additional_points(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ClusteringBiasOfAdditionalPoints", value)

    @property
    @exception_bridge
    def logarithmic_frequency_axis(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "LogarithmicFrequencyAxis")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @logarithmic_frequency_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def logarithmic_frequency_axis(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LogarithmicFrequencyAxis", value)

    @property
    @exception_bridge
    def maximum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Maximum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Maximum", value)

    @property
    @exception_bridge
    def minimum(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "Minimum")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "Minimum", value)

    @property
    @exception_bridge
    def number_of_points_across_range(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPointsAcrossRange")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_across_range.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_across_range(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfPointsAcrossRange", value)

    @property
    @exception_bridge
    def number_of_points_per_step_for_torque_map(
        self: "Self",
    ) -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPointsPerStepForTorqueMap")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_points_per_step_for_torque_map.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_points_per_step_for_torque_map(
        self: "Self", value: "Union[int, Tuple[int, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfPointsPerStepForTorqueMap", value)

    @property
    @exception_bridge
    def use_logarithmic_spacing(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "UseLogarithmicSpacing")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @use_logarithmic_spacing.setter
    @exception_bridge
    @enforce_parameter_types
    def use_logarithmic_spacing(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "UseLogarithmicSpacing", value)

    @property
    @exception_bridge
    def design_defaults(self: "Self") -> "FrequencyOptionsForHarmonicAnalysisResults":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.FrequencyOptionsForHarmonicAnalysisResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DesignDefaults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_FrequencyOptionsForHarmonicAnalysisResults":
        """Cast to another type.

        Returns:
            _Cast_FrequencyOptionsForHarmonicAnalysisResults
        """
        return _Cast_FrequencyOptionsForHarmonicAnalysisResults(self)
