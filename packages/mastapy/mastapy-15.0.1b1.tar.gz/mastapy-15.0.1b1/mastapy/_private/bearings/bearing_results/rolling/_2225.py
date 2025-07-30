"""LoadedFourPointContactBallBearingResults"""

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
from mastapy._private.bearings.bearing_results.rolling import _2210

_LOADED_FOUR_POINT_CONTACT_BALL_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedFourPointContactBallBearingResults",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings import _2078
    from mastapy._private.bearings.bearing_results import _2155, _2160, _2163
    from mastapy._private.bearings.bearing_results.rolling import _2179, _2241

    Self = TypeVar("Self", bound="LoadedFourPointContactBallBearingResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedFourPointContactBallBearingResults._Cast_LoadedFourPointContactBallBearingResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedFourPointContactBallBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedFourPointContactBallBearingResults:
    """Special nested class for casting LoadedFourPointContactBallBearingResults to subclasses."""

    __parent__: "LoadedFourPointContactBallBearingResults"

    @property
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2210.LoadedBallBearingResults":
        return self.__parent__._cast(_2210.LoadedBallBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2241.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2241

        return self.__parent__._cast(_2241.LoadedRollingBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "_2155.LoadedBearingResults":
        from mastapy._private.bearings.bearing_results import _2155

        return self.__parent__._cast(_2155.LoadedBearingResults)

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        from mastapy._private.bearings import _2078

        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "LoadedFourPointContactBallBearingResults":
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
class LoadedFourPointContactBallBearingResults(_2210.LoadedBallBearingResults):
    """LoadedFourPointContactBallBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_FOUR_POINT_CONTACT_BALL_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def raceway_control(self: "Self") -> "_2179.FrictionModelForGyroscopicMoment":
        """mastapy.bearings.bearing_results.rolling.FrictionModelForGyroscopicMoment

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RacewayControl")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingResults.Rolling.FrictionModelForGyroscopicMoment",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results.rolling._2179",
            "FrictionModelForGyroscopicMoment",
        )(value)

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedFourPointContactBallBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedFourPointContactBallBearingResults
        """
        return _Cast_LoadedFourPointContactBallBearingResults(self)
