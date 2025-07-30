"""HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6170,
)

_HARMONIC_ANALYSIS_COMBINED_FOR_MULTIPLE_SURFACES_WITHIN_A_HARMONIC = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6168,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic._Cast_HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic:
    """Special nested class for casting HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic to subclasses."""

    __parent__: "HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic"

    @property
    def harmonic_analysis_results_broken_down_by_surface_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic":
        return self.__parent__._cast(
            _6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
        )

    @property
    def harmonic_analysis_results_broken_down_by_location_within_a_harmonic(
        self: "CastSelf",
    ) -> "_6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6168,
        )

        return self.__parent__._cast(
            _6168.HarmonicAnalysisResultsBrokenDownByLocationWithinAHarmonic
        )

    @property
    def harmonic_analysis_combined_for_multiple_surfaces_within_a_harmonic(
        self: "CastSelf",
    ) -> "HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic":
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
class HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic(
    _6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic
):
    """HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_COMBINED_FOR_MULTIPLE_SURFACES_WITHIN_A_HARMONIC
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def surface_names(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceNames")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic
        """
        return _Cast_HarmonicAnalysisCombinedForMultipleSurfacesWithinAHarmonic(self)
