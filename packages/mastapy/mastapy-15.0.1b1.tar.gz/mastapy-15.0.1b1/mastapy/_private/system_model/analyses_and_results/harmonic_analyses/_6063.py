"""HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"""

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
from mastapy._private.system_model.analyses_and_results.static_loads import _7674

_HARMONIC_ANALYSIS_WITH_VARYING_STIFFNESS_STATIC_LOAD_CASE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2891
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6058,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7673

    Self = TypeVar("Self", bound="HarmonicAnalysisWithVaryingStiffnessStaticLoadCase")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisWithVaryingStiffnessStaticLoadCase._Cast_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisWithVaryingStiffnessStaticLoadCase",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase:
    """Special nested class for casting HarmonicAnalysisWithVaryingStiffnessStaticLoadCase to subclasses."""

    __parent__: "HarmonicAnalysisWithVaryingStiffnessStaticLoadCase"

    @property
    def static_load_case(self: "CastSelf") -> "_7674.StaticLoadCase":
        return self.__parent__._cast(_7674.StaticLoadCase)

    @property
    def load_case(self: "CastSelf") -> "_7673.LoadCase":
        from mastapy._private.system_model.analyses_and_results.static_loads import (
            _7673,
        )

        return self.__parent__._cast(_7673.LoadCase)

    @property
    def context(self: "CastSelf") -> "_2891.Context":
        from mastapy._private.system_model.analyses_and_results import _2891

        return self.__parent__._cast(_2891.Context)

    @property
    def harmonic_analysis_with_varying_stiffness_static_load_case(
        self: "CastSelf",
    ) -> "HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
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
class HarmonicAnalysisWithVaryingStiffnessStaticLoadCase(_7674.StaticLoadCase):
    """HarmonicAnalysisWithVaryingStiffnessStaticLoadCase

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_WITH_VARYING_STIFFNESS_STATIC_LOAD_CASE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def harmonic_analysis_options(self: "Self") -> "_6058.HarmonicAnalysisOptions":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.HarmonicAnalysisOptions

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HarmonicAnalysisOptions")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase
        """
        return _Cast_HarmonicAnalysisWithVaryingStiffnessStaticLoadCase(self)
