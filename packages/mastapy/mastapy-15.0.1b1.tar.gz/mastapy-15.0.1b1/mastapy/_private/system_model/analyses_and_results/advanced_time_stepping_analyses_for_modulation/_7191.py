"""HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6058

_HARMONIC_ANALYSIS_OPTIONS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar(
        "Self",
        bound="HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation",
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation._Cast_HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation"

    @property
    def harmonic_analysis_options(self: "CastSelf") -> "_6058.HarmonicAnalysisOptions":
        return self.__parent__._cast(_6058.HarmonicAnalysisOptions)

    @property
    def harmonic_analysis_options_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation":
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
class HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation(
    _6058.HarmonicAnalysisOptions
):
    """HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_OPTIONS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation
        """
        return (
            _Cast_HarmonicAnalysisOptionsForAdvancedTimeSteppingAnalysisForModulation(
                self
            )
        )
