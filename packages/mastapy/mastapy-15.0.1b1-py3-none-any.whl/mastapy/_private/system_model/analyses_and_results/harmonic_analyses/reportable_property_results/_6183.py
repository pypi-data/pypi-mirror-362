"""RootAssemblySingleWhineAnalysisResultsPropertyAccessor"""

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
from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
    _6160,
)

_ROOT_ASSEMBLY_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "RootAssemblySingleWhineAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6176,
    )

    Self = TypeVar(
        "Self", bound="RootAssemblySingleWhineAnalysisResultsPropertyAccessor"
    )
    CastSelf = TypeVar(
        "CastSelf",
        bound="RootAssemblySingleWhineAnalysisResultsPropertyAccessor._Cast_RootAssemblySingleWhineAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RootAssemblySingleWhineAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RootAssemblySingleWhineAnalysisResultsPropertyAccessor:
    """Special nested class for casting RootAssemblySingleWhineAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "RootAssemblySingleWhineAnalysisResultsPropertyAccessor"

    @property
    def abstract_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6160.AbstractSingleWhineAnalysisResultsPropertyAccessor":
        return self.__parent__._cast(
            _6160.AbstractSingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def root_assembly_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "RootAssemblySingleWhineAnalysisResultsPropertyAccessor":
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
class RootAssemblySingleWhineAnalysisResultsPropertyAccessor(
    _6160.AbstractSingleWhineAnalysisResultsPropertyAccessor
):
    """RootAssemblySingleWhineAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = (
        _ROOT_ASSEMBLY_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR
    )

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def orders(self: "Self") -> "List[_6176.ResultsForOrderIncludingGroups]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.ResultsForOrderIncludingGroups]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Orders")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_RootAssemblySingleWhineAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_RootAssemblySingleWhineAnalysisResultsPropertyAccessor
        """
        return _Cast_RootAssemblySingleWhineAnalysisResultsPropertyAccessor(self)
