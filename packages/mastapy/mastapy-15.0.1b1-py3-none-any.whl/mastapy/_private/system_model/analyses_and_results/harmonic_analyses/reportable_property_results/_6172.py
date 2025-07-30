"""ResultsForMultipleOrders"""

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

_RESULTS_FOR_MULTIPLE_ORDERS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.ReportablePropertyResults",
    "ResultsForMultipleOrders",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
        _6173,
        _6174,
    )

    Self = TypeVar("Self", bound="ResultsForMultipleOrders")
    CastSelf = TypeVar(
        "CastSelf", bound="ResultsForMultipleOrders._Cast_ResultsForMultipleOrders"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ResultsForMultipleOrders",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ResultsForMultipleOrders:
    """Special nested class for casting ResultsForMultipleOrders to subclasses."""

    __parent__: "ResultsForMultipleOrders"

    @property
    def results_for_multiple_orders_for_fe_surface(
        self: "CastSelf",
    ) -> "_6173.ResultsForMultipleOrdersForFESurface":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6173,
        )

        return self.__parent__._cast(_6173.ResultsForMultipleOrdersForFESurface)

    @property
    def results_for_multiple_orders_for_groups(
        self: "CastSelf",
    ) -> "_6174.ResultsForMultipleOrdersForGroups":
        from mastapy._private.system_model.analyses_and_results.harmonic_analyses.reportable_property_results import (
            _6174,
        )

        return self.__parent__._cast(_6174.ResultsForMultipleOrdersForGroups)

    @property
    def results_for_multiple_orders(self: "CastSelf") -> "ResultsForMultipleOrders":
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
class ResultsForMultipleOrders(_0.APIBase):
    """ResultsForMultipleOrders

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RESULTS_FOR_MULTIPLE_ORDERS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combined_excitations_harmonics_and_orders(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CombinedExcitationsHarmonicsAndOrders"
        )

        if temp is None:
            return ""

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ResultsForMultipleOrders":
        """Cast to another type.

        Returns:
            _Cast_ResultsForMultipleOrders
        """
        return _Cast_ResultsForMultipleOrders(self)
