"""ResultsForMultipleOrdersForFESurface"""

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
    _6172,
)

_RESULTS_FOR_MULTIPLE_ORDERS_FOR_FE_SURFACE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForMultipleOrdersForFESurface",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6170,
    )

    Self = TypeVar("Self", bound="ResultsForMultipleOrdersForFESurface")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ResultsForMultipleOrdersForFESurface._Cast_ResultsForMultipleOrdersForFESurface",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForMultipleOrdersForFESurface",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForMultipleOrdersForFESurface:
    """Special nested class for casting ResultsForMultipleOrdersForFESurface to subclasses."""

    __parent__: "ResultsForMultipleOrdersForFESurface"

    @property
    def results_for_multiple_orders(
        self: "CastSelf",
    ) -> "_6172.ResultsForMultipleOrders":
        return self.__parent__._cast(_6172.ResultsForMultipleOrders)

    @property
    def results_for_multiple_orders_for_fe_surface(
        self: "CastSelf",
    ) -> "ResultsForMultipleOrdersForFESurface":
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
class ResultsForMultipleOrdersForFESurface(_6172.ResultsForMultipleOrders):
    """ResultsForMultipleOrdersForFESurface

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_MULTIPLE_ORDERS_FOR_FE_SURFACE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def default_fe_surface(
        self: "Self",
    ) -> "_6170.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic":
        """mastapy.system_model.analyses_and_results.harmonic_analyses.reportable_property_results.HarmonicAnalysisResultsBrokenDownBySurfaceWithinAHarmonic

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DefaultFESurface")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_ResultsForMultipleOrdersForFESurface":
        """Cast to another type.

        Returns:
            _Cast_ResultsForMultipleOrdersForFESurface
        """
        return _Cast_ResultsForMultipleOrdersForFESurface(self)
