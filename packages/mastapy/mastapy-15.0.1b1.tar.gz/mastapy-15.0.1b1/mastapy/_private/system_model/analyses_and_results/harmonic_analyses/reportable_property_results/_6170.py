"""HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6168,
)

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6165,
        _6179,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic._Cast_HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic:
    """Special nested class for casting HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic to subclasses."""

    __parent__: "HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic"

    @property
    def harmonic_analysis_results_broken_down_by_location_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
        return self.__parent__._cast(
            _6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
        )

    @property
    def harmonic_analysis_combined_for_multiple_surfaces_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6165.HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6165,
        )

        return self.__parent__._cast(
            _6165.HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_surface_within_a_harmonic(
        self: "CastSelf",
    ) -> "HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic":
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
class HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic(
    _6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
):
    """HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_SURFACE_WITHIN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def surface_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def airborne_sound_power_erp(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AirborneSoundPowerERP")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def maximum_normal_velocity(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalVelocity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_mean_squared_normal_acceleration(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootMeanSquaredNormalAcceleration")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_mean_squared_normal_displacement(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootMeanSquaredNormalDisplacement")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def root_mean_squared_normal_velocity(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootMeanSquaredNormalVelocity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_intensity_from_erp(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundIntensityFromERP")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_pressure_from_erp(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundPressureFromERP")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
        """
        return _Cast_HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic(self)
