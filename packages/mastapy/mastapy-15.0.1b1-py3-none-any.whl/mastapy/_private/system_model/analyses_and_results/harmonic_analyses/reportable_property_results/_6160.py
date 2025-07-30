"""AbstractSingleWhineAnalysisResultsPropertyAccessor"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_ABSTRACT_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "AbstractSingleWhineAnalysisResultsPropertyAccessor",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6164,
        _6183,
        _6184,
    )

    Self = TypeVar("Self", bound="AbstractSingleWhineAnalysisResultsPropertyAccessor")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AbstractSingleWhineAnalysisResultsPropertyAccessor._Cast_AbstractSingleWhineAnalysisResultsPropertyAccessor",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AbstractSingleWhineAnalysisResultsPropertyAccessor",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractSingleWhineAnalysisResultsPropertyAccessor:
    """Special nested class for casting AbstractSingleWhineAnalysisResultsPropertyAccessor to subclasses."""

    __parent__: "AbstractSingleWhineAnalysisResultsPropertyAccessor"

    @property
    def fe_part_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6164.FEPartSingleWhineAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6164,
        )

        return self.__parent__._cast(
            _6164.FEPartSingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def root_assembly_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6183.RootAssemblySingleWhineAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6183,
        )

        return self.__parent__._cast(
            _6183.RootAssemblySingleWhineAnalysisResultsPropertyAccessor
        )

    @property
    def single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "_6184.SingleWhineAnalysisResultsPropertyAccessor":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6184,
        )

        return self.__parent__._cast(_6184.SingleWhineAnalysisResultsPropertyAccessor)

    @property
    def abstract_single_whine_analysis_results_property_accessor(
        self: "CastSelf",
    ) -> "AbstractSingleWhineAnalysisResultsPropertyAccessor":
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
class AbstractSingleWhineAnalysisResultsPropertyAccessor(_0.APIBase):
    """AbstractSingleWhineAnalysisResultsPropertyAccessor

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_SINGLE_WHINE_ANALYSIS_RESULTS_PROPERTY_ACCESSOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_AbstractSingleWhineAnalysisResultsPropertyAccessor":
        """Cast to another type.

        Returns:
            _Cast_AbstractSingleWhineAnalysisResultsPropertyAccessor
        """
        return _Cast_AbstractSingleWhineAnalysisResultsPropertyAccessor(self)
