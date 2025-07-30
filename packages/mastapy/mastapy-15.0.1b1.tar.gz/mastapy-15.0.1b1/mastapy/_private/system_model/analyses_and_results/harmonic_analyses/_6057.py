"""HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.analyses_and_results.harmonic_analyses import _6052

_HARMONIC_ANALYSIS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = (
    python_net_import(
        "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
        "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    )
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7877,
        _7879,
        _7892,
    )

    Self = TypeVar(
        "Self", bound="HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation._Cast_HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation:
    """Special nested class for casting HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation to subclasses."""

    __parent__: "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation"

    @property
    def harmonic_analysis(self: "CastSelf") -> "_6052.HarmonicAnalysis":
        return self.__parent__._cast(_6052.HarmonicAnalysis)

    @property
    def compound_analysis_case(self: "CastSelf") -> "_7879.CompoundAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7879,
        )

        return self.__parent__._cast(_7879.CompoundAnalysisCase)

    @property
    def static_load_analysis_case(self: "CastSelf") -> "_7892.StaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7892,
        )

        return self.__parent__._cast(_7892.StaticLoadAnalysisCase)

    @property
    def analysis_case(self: "CastSelf") -> "_7877.AnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7877,
        )

        return self.__parent__._cast(_7877.AnalysisCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def harmonic_analysis_for_advanced_time_stepping_analysis_for_modulation(
        self: "CastSelf",
    ) -> "HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
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
class HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation(
    _6052.HarmonicAnalysis
):
    """HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _HARMONIC_ANALYSIS_FOR_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation
        """
        return _Cast_HarmonicAnalysisForAdvancedTimeSteppingAnalysisForModulation(self)
