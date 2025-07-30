"""SynchroniserSleeveCompoundHarmonicAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
    _6302,
)

_SYNCHRONISER_SLEEVE_COMPOUND_HARMONIC_ANALYSIS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Compound",
    "SynchroniserSleeveCompoundHarmonicAnalysis",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses import (
        _6126,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
        _6210,
        _6224,
        _6264,
        _6266,
    )
    from mastapy._private.system_model.part_model.couplings import _2852

    Self = TypeVar("Self", bound="SynchroniserSleeveCompoundHarmonicAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SynchroniserSleeveCompoundHarmonicAnalysis._Cast_SynchroniserSleeveCompoundHarmonicAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SynchroniserSleeveCompoundHarmonicAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SynchroniserSleeveCompoundHarmonicAnalysis:
    """Special nested class for casting SynchroniserSleeveCompoundHarmonicAnalysis to subclasses."""

    __parent__: "SynchroniserSleeveCompoundHarmonicAnalysis"

    @property
    def synchroniser_part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6302.SynchroniserPartCompoundHarmonicAnalysis":
        return self.__parent__._cast(_6302.SynchroniserPartCompoundHarmonicAnalysis)

    @property
    def coupling_half_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6224.CouplingHalfCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6224,
        )

        return self.__parent__._cast(_6224.CouplingHalfCompoundHarmonicAnalysis)

    @property
    def mountable_component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6264.MountableComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6264,
        )

        return self.__parent__._cast(_6264.MountableComponentCompoundHarmonicAnalysis)

    @property
    def component_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6210.ComponentCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6210,
        )

        return self.__parent__._cast(_6210.ComponentCompoundHarmonicAnalysis)

    @property
    def part_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "_6266.PartCompoundHarmonicAnalysis":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.compound import (
            _6266,
        )

        return self.__parent__._cast(_6266.PartCompoundHarmonicAnalysis)

    @property
    def part_compound_analysis(self: "CastSelf") -> "_7888.PartCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7888,
        )

        return self.__parent__._cast(_7888.PartCompoundAnalysis)

    @property
    def design_entity_compound_analysis(
        self: "CastSelf",
    ) -> "_7885.DesignEntityCompoundAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7885,
        )

        return self.__parent__._cast(_7885.DesignEntityCompoundAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def synchroniser_sleeve_compound_harmonic_analysis(
        self: "CastSelf",
    ) -> "SynchroniserSleeveCompoundHarmonicAnalysis":
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
class SynchroniserSleeveCompoundHarmonicAnalysis(
    _6302.SynchroniserPartCompoundHarmonicAnalysis
):
    """SynchroniserSleeveCompoundHarmonicAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SYNCHRONISER_SLEEVE_COMPOUND_HARMONIC_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def component_design(self: "Self") -> "_2852.SynchroniserSleeve":
        """mastapy.system_model.part_model.couplings.SynchroniserSleeve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6126.SynchroniserSleeveHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SynchroniserSleeveHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def component_analysis_cases(
        self: "Self",
    ) -> "List[_6126.SynchroniserSleeveHarmonicAnalysis]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.SynchroniserSleeveHarmonicAnalysis]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_SynchroniserSleeveCompoundHarmonicAnalysis":
        """Cast to another type.

        Returns:
            _Cast_SynchroniserSleeveCompoundHarmonicAnalysis
        """
        return _Cast_SynchroniserSleeveCompoundHarmonicAnalysis(self)
