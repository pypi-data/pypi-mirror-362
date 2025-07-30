"""TrackTruncationSafetyFactorResults"""

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

_TRACK_TRUNCATION_SAFETY_FACTOR_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "TrackTruncationSafetyFactorResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TrackTruncationSafetyFactorResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="TrackTruncationSafetyFactorResults._Cast_TrackTruncationSafetyFactorResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("TrackTruncationSafetyFactorResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TrackTruncationSafetyFactorResults:
    """Special nested class for casting TrackTruncationSafetyFactorResults to subclasses."""

    __parent__: "TrackTruncationSafetyFactorResults"

    @property
    def track_truncation_safety_factor_results(
        self: "CastSelf",
    ) -> "TrackTruncationSafetyFactorResults":
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
class TrackTruncationSafetyFactorResults(_0.APIBase):
    """TrackTruncationSafetyFactorResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRACK_TRUNCATION_SAFETY_FACTOR_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def element_with_worst_track_truncation(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementWithWorstTrackTruncation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def smallest_arc_distance_of_raceway_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SmallestArcDistanceOfRacewayEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def track_truncation_occurring_beyond_permissible_limit(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TrackTruncationOccurringBeyondPermissibleLimit"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def worst_hertzian_ellipse_major_2b_track_truncation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstHertzianEllipseMajor2bTrackTruncation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_hertzian_ellipse_major_2b_track_truncation_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstHertzianEllipseMajor2bTrackTruncationInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_hertzian_ellipse_major_2b_track_truncation_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstHertzianEllipseMajor2bTrackTruncationOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_TrackTruncationSafetyFactorResults":
        """Cast to another type.

        Returns:
            _Cast_TrackTruncationSafetyFactorResults
        """
        return _Cast_TrackTruncationSafetyFactorResults(self)
