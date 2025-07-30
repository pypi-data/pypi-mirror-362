"""LoadedFourPointContactBallBearingRow"""

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
from mastapy._private.bearings.bearing_results.rolling import _2211

_LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ROW = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedFourPointContactBallBearingRow",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2224, _2225, _2242

    Self = TypeVar("Self", bound="LoadedFourPointContactBallBearingRow")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedFourPointContactBallBearingRow._Cast_LoadedFourPointContactBallBearingRow",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedFourPointContactBallBearingRow",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedFourPointContactBallBearingRow:
    """Special nested class for casting LoadedFourPointContactBallBearingRow to subclasses."""

    __parent__: "LoadedFourPointContactBallBearingRow"

    @property
    def loaded_ball_bearing_row(self: "CastSelf") -> "_2211.LoadedBallBearingRow":
        return self.__parent__._cast(_2211.LoadedBallBearingRow)

    @property
    def loaded_rolling_bearing_row(self: "CastSelf") -> "_2242.LoadedRollingBearingRow":
        from mastapy._private.bearings.bearing_results.rolling import _2242

        return self.__parent__._cast(_2242.LoadedRollingBearingRow)

    @property
    def loaded_four_point_contact_ball_bearing_row(
        self: "CastSelf",
    ) -> "LoadedFourPointContactBallBearingRow":
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
class LoadedFourPointContactBallBearingRow(_2211.LoadedBallBearingRow):
    """LoadedFourPointContactBallBearingRow

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ROW

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def loaded_bearing(
        self: "Self",
    ) -> "_2225.LoadedFourPointContactBallBearingResults":
        """mastapy.bearings.bearing_results.rolling.LoadedFourPointContactBallBearingResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadedBearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def race_results(
        self: "Self",
    ) -> "List[_2224.LoadedFourPointContactBallBearingRaceResults]":
        """List[mastapy.bearings.bearing_results.rolling.LoadedFourPointContactBallBearingRaceResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedFourPointContactBallBearingRow":
        """Cast to another type.

        Returns:
            _Cast_LoadedFourPointContactBallBearingRow
        """
        return _Cast_LoadedFourPointContactBallBearingRow(self)
