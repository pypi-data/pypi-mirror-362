"""RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
    _6456,
)

_ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalysesSingleExcitation.Compound",
    "RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results import _2892
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7885,
        _7888,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation import (
        _6414,
    )
    from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
        _6449,
        _6530,
    )

    Self = TypeVar(
        "Self", bound="RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation._Cast_RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation:
    """Special nested class for casting RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation to subclasses."""

    __parent__: "RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation"

    @property
    def assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6456.AssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        return self.__parent__._cast(
            _6456.AssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def abstract_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6449.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6449,
        )

        return self.__parent__._cast(
            _6449.AbstractAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        )

    @property
    def part_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "_6530.PartCompoundHarmonicAnalysisOfSingleExcitation":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses_single_excitation.compound import (
            _6530,
        )

        return self.__parent__._cast(
            _6530.PartCompoundHarmonicAnalysisOfSingleExcitation
        )

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
    def root_assembly_compound_harmonic_analysis_of_single_excitation(
        self: "CastSelf",
    ) -> "RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
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
class RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation(
    _6456.AssemblyCompoundHarmonicAnalysisOfSingleExcitation
):
    """RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ROOT_ASSEMBLY_COMPOUND_HARMONIC_ANALYSIS_OF_SINGLE_EXCITATION
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def assembly_analysis_cases_ready(
        self: "Self",
    ) -> "List[_6414.RootAssemblyHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.RootAssemblyHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCasesReady")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def assembly_analysis_cases(
        self: "Self",
    ) -> "List[_6414.RootAssemblyHarmonicAnalysisOfSingleExcitation]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses_single_excitation.RootAssemblyHarmonicAnalysisOfSingleExcitation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AssemblyAnalysisCases")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation
        """
        return _Cast_RootAssemblyCompoundHarmonicAnalysisOfSingleExcitation(self)
