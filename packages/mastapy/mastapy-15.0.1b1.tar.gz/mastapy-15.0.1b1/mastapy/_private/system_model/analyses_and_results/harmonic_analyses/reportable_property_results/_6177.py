"""ResultsForOrderIncludingNodes"""

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
    _6175,
)

_RESULTS_FOR_ORDER_INCLUDING_NODES = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForOrderIncludingNodes",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6169,
        _6178,
    )

    Self = TypeVar("Self", bound="ResultsForOrderIncludingNodes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForOrderIncludingNodes._Cast_ResultsForOrderIncludingNodes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForOrderIncludingNodes",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForOrderIncludingNodes:
    """Special nested class for casting ResultsForOrderIncludingNodes to subclasses."""

    __parent__: "ResultsForOrderIncludingNodes"

    @property
    def results_for_order(self: "CastSelf") -> "_6175.ResultsForOrder":
        return self.__parent__._cast(_6175.ResultsForOrder)

    @property
    def results_for_order_including_surfaces(
        self: "CastSelf",
    ) -> "_6178.ResultsForOrderIncludingSurfaces":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6178,
        )

        return self.__parent__._cast(_6178.ResultsForOrderIncludingSurfaces)

    @property
    def results_for_order_including_nodes(
        self: "CastSelf",
    ) -> "ResultsForOrderIncludingNodes":
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
class ResultsForOrderIncludingNodes(_6175.ResultsForOrder):
    """ResultsForOrderIncludingNodes

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_ORDER_INCLUDING_NODES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def node_results_global_coordinate_system(
        self: "Self",
    ) -> "List[_6169.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeResultsGlobalCoordinateSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def node_results_local_coordinate_system(
        self: "Self",
    ) -> "List[_6169.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]":
        """List[mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownByNodeWithinAHarmonic]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NodeResultsLocalCoordinateSystem")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_ResultsForOrderIncludingNodes":
        """Cast to another type.

        Returns:
            _Cast_ResultsForOrderIncludingNodes
        """
        return _Cast_ResultsForOrderIncludingNodes(self)
