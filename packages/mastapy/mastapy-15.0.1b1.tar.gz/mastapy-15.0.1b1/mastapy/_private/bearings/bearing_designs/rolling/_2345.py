"""AngularContactBallBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2350

_ANGULAR_CONTACT_BALL_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "AngularContactBallBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import _2346, _2375

    Self = TypeVar("Self", bound="AngularContactBallBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="AngularContactBallBearing._Cast_AngularContactBallBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AngularContactBallBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AngularContactBallBearing:
    """Special nested class for casting AngularContactBallBearing to subclasses."""

    __parent__: "AngularContactBallBearing"

    @property
    def ball_bearing(self: "CastSelf") -> "_2350.BallBearing":
        return self.__parent__._cast(_2350.BallBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2375

        return self.__parent__._cast(_2375.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2346.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2346

        return self.__parent__._cast(_2346.AngularContactThrustBallBearing)

    @property
    def angular_contact_ball_bearing(self: "CastSelf") -> "AngularContactBallBearing":
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
class AngularContactBallBearing(_2350.BallBearing):
    """AngularContactBallBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ANGULAR_CONTACT_BALL_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AngularContactBallBearing":
        """Cast to another type.

        Returns:
            _Cast_AngularContactBallBearing
        """
        return _Cast_AngularContactBallBearing(self)
