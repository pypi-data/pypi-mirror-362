"""FEPartHarmonicAnalysisResultsPropertyAccessor"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6171,
)

_FE_PART_HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "FEPartHarmonicAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6164,
        _6173,
        _6178,
    )

    Self = TypeVar("Self", bound="FEPartHarmonicAnalysisResultsPropertyAccessor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FEPartHarmonicAnalysisResultsPropertyAccessor._Cast_FEPartHarmonicAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEPartHarmonicAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FEPartHarmonicAnalysisResultsPropertyAccessor:
    """Special nested class for casting FEPartHarmonicAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "FEPartHarmonicAnalysisResultsPropertyAccessor"

    @property
    def harmonic_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6171.HarmonicAnalysisResultsPropertyAccessor":
        return self.__parent__._cast(_6171.HarmonicAnalysisResultsPropertyAccessor)

    @property
    def fe_part_harmonic_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "FEPartHarmonicAnalysisResultsPropertyAccessor":
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
class FEPartHarmonicAnalysisResultsPropertyAccessor(
    _6171.HarmonicAnalysisResultsPropertyAccessor
):
    """FEPartHarmonicAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FE_PART_HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combined_orders(self: "Self") -> "_6173.ResultsForMultipleOrdersForFESurface":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForMultipleOrdersForFESurface

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedOrders")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def excitations(
        self: "Self",
    ) -> "List[_6164.FEPartSingleWhineAnalysisResultsPropertyAccessor]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.FEPartSingleWhineAnalysisResultsPropertyAccessor]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Excitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def orders_for_combined_excitations(
        self: "Self",
    ) -> "List[_6178.ResultsForOrderIncludingSurfaces]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingSurfaces]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OrdersForCombinedExcitations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def orders_for_combined_excitations_from_same_parts(
        self: "Self",
    ) -> "List[_6178.ResultsForOrderIncludingSurfaces]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingSurfaces]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OrdersForCombinedExcitationsFromSameParts"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FEPartHarmonicAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_FEPartHarmonicAnalysisResultsPropertyAccessor
        """
        return _Cast_FEPartHarmonicAnalysisResultsPropertyAccessor(self)
