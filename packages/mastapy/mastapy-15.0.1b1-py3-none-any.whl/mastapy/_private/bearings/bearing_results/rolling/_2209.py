"""LoadedBallBearingRaceResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2240

_LOADED_BALL_BEARING_RACE_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedBallBearingRaceResults"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2224

    Self = TypeVar("Self", bound="LoadedBallBearingRaceResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedBallBearingRaceResults._Cast_LoadedBallBearingRaceResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBallBearingRaceResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBallBearingRaceResults:
    """Special nested class for casting LoadedBallBearingRaceResults to subclasses."""

    __parent__: "LoadedBallBearingRaceResults"

    @property
    def loaded_rolling_bearing_race_results(
        self: "CastSelf",
    ) -> "_2240.LoadedRollingBearingRaceResults":
        return self.__parent__._cast(_2240.LoadedRollingBearingRaceResults)

    @property
    def loaded_four_point_contact_ball_bearing_race_results(
        self: "CastSelf",
    ) -> "_2224.LoadedFourPointContactBallBearingRaceResults":
        from mastapy._private.bearings.bearing_results.rolling import _2224

        return self.__parent__._cast(_2224.LoadedFourPointContactBallBearingRaceResults)

    @property
    def loaded_ball_bearing_race_results(
        self: "CastSelf",
    ) -> "LoadedBallBearingRaceResults":
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
class LoadedBallBearingRaceResults(_2240.LoadedRollingBearingRaceResults):
    """LoadedBallBearingRaceResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BALL_BEARING_RACE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_radius_at_right_angles_to_rolling_direction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusAtRightAnglesToRollingDirection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_highest_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMajorDimensionHighestLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_highest_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMinorDimensionHighestLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBallBearingRaceResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedBallBearingRaceResults
        """
        return _Cast_LoadedBallBearingRaceResults(self)
