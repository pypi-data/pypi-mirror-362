"""HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic"""

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

_HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6179,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic._Cast_HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic:
    """Special nested class for casting HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic to subclasses."""

    __parent__: "HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic"

    @property
    def harmonic_analysis_results_broken_down_by_location_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
        return self.__parent__._cast(
            _6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_component_within_a_harmonic(
        self: "CastSelf",
    ) -> "HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic":
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
class HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic(
    _6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
):
    """HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_RESULTS_BROKEN_DOWN_BY_COMPONENT_WITHIN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def dynamic_mesh_force(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicMeshForce")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def dynamic_mesh_moment(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicMeshMoment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def dynamic_misalignment(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicMisalignment")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def dynamic_te(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicTE")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def kinetic_energy(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KineticEnergy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_intensity(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundIntensity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_pressure(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundPressure")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sound_velocity(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SoundVelocity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def strain_energy(
        self: "Self",
    ) -> "_6179.ResultsForResponseOfAComponentOrSurfaceInAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForResponseOfAComponentOrSurfaceInAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrainEnergy")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic
        """
        return _Cast_HarmonicAnalysisResultsBrokenDownByComponentWithinAHarmonic(self)
