"""HarmonicAnalysisResultsPropertyAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "HarmonicAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6163,
        _6177,
        _6184,
    )

    Self = TypeVar("Self", bound="HarmonicAnalysisResultsPropertyAccessor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisResultsPropertyAccessor._Cast_HarmonicAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HarmonicAnalysisResultsPropertyAccessor:
    """Special nested class for casting HarmonicAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "HarmonicAnalysisResultsPropertyAccessor"

    @property
    def fe_part_harmonic_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6163.FEPartHarmonicAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6163,
        )

        return self.__parent__._cast(
            _6163.FEPartHarmonicAnalysisResultsPropertyAccessor
        )

    @property
    def harmonic_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "HarmonicAnalysisResultsPropertyAccessor":
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
class HarmonicAnalysisResultsPropertyAccessor(_0.APIBase):
    """HarmonicAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HARMONIC_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def excitations(
        self: "Self",
    ) -> "List[_6184.SingleWhineAnalysisResultsPropertyAccessor]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.SingleWhineAnalysisResultsPropertyAccessor]

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
    ) -> "List[_6177.ResultsForOrderIncludingNodes]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingNodes]

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
    ) -> "List[_6177.ResultsForOrderIncludingNodes]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingNodes]

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
    def cast_to(self: "Self") -> "_Cast_HarmonicAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_HarmonicAnalysisResultsPropertyAccessor
        """
        return _Cast_HarmonicAnalysisResultsPropertyAccessor(self)
