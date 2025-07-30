"""LoadedFourPointContactBallBearingRaceResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2209

_LOADED_FOUR_POINT_CONTACT_BALL_BEARING_RACE_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedFourPointContactBallBearingRaceResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2240

    Self = TypeVar("Self", bound="LoadedFourPointContactBallBearingRaceResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedFourPointContactBallBearingRaceResults._Cast_LoadedFourPointContactBallBearingRaceResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedFourPointContactBallBearingRaceResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedFourPointContactBallBearingRaceResults:
    """Special nested class for casting LoadedFourPointContactBallBearingRaceResults to subclasses."""

    __parent__: "LoadedFourPointContactBallBearingRaceResults"

    @property
    def loaded_ball_bearing_race_results(
        self: "CastSelf",
    ) -> "_2209.LoadedBallBearingRaceResults":
        return self.__parent__._cast(_2209.LoadedBallBearingRaceResults)

    @property
    def loaded_rolling_bearing_race_results(
        self: "CastSelf",
    ) -> "_2240.LoadedRollingBearingRaceResults":
        from mastapy._private.bearings.bearing_results.rolling import _2240

        return self.__parent__._cast(_2240.LoadedRollingBearingRaceResults)

    @property
    def loaded_four_point_contact_ball_bearing_race_results(
        self: "CastSelf",
    ) -> "LoadedFourPointContactBallBearingRaceResults":
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
class LoadedFourPointContactBallBearingRaceResults(_2209.LoadedBallBearingRaceResults):
    """LoadedFourPointContactBallBearingRaceResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_FOUR_POINT_CONTACT_BALL_BEARING_RACE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedFourPointContactBallBearingRaceResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedFourPointContactBallBearingRaceResults
        """
        return _Cast_LoadedFourPointContactBallBearingRaceResults(self)
