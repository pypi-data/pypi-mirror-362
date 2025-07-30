"""ResultsForOrderIncludingSurfaces"""

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
    _6177,
)

_RESULTS_FOR_ORDER_INCLUDING_SURFACES = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForOrderIncludingSurfaces",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6170,
        _6175,
    )

    Self = TypeVar("Self", bound="ResultsForOrderIncludingSurfaces")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForOrderIncludingSurfaces._Cast_ResultsForOrderIncludingSurfaces",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForOrderIncludingSurfaces",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForOrderIncludingSurfaces:
    """Special nested class for casting ResultsForOrderIncludingSurfaces to subclasses."""

    __parent__: "ResultsForOrderIncludingSurfaces"

    @property
    def results_for_order_including_nodes(
        self: "CastSelf",
    ) -> "_6177.ResultsForOrderIncludingNodes":
        return self.__parent__._cast(_6177.ResultsForOrderIncludingNodes)

    @property
    def results_for_order(self: "CastSelf") -> "_6175.ResultsForOrder":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6175,
        )

        return self.__parent__._cast(_6175.ResultsForOrder)

    @property
    def results_for_order_including_surfaces(
        self: "CastSelf",
    ) -> "ResultsForOrderIncludingSurfaces":
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
class ResultsForOrderIncludingSurfaces(_6177.ResultsForOrderIncludingNodes):
    """ResultsForOrderIncludingSurfaces

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_ORDER_INCLUDING_SURFACES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def fe_surfaces(
        self: "Self",
    ) -> "List[_6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FESurfaces")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ResultsForOrderIncludingSurfaces":
        """Cast to another type.

        Returns:
            _Cast_ResultsForOrderIncludingSurfaces
        """
        return _Cast_ResultsForOrderIncludingSurfaces(self)
