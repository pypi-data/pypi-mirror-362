"""LoadedAngularContactThrustBallBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_results.rolling import _2190

_LOADED_ANGULAR_CONTACT_THRUST_BALL_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedAngularContactThrustBallBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2208, _2222

    Self = TypeVar("Self", bound="LoadedAngularContactThrustBallBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedAngularContactThrustBallBearingElement._Cast_LoadedAngularContactThrustBallBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedAngularContactThrustBallBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedAngularContactThrustBallBearingElement:
    """Special nested class for casting LoadedAngularContactThrustBallBearingElement to subclasses."""

    __parent__: "LoadedAngularContactThrustBallBearingElement"

    @property
    def loaded_angular_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2190.LoadedAngularContactBallBearingElement":
        return self.__parent__._cast(_2190.LoadedAngularContactBallBearingElement)

    @property
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2208.LoadedBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2208

        return self.__parent__._cast(_2208.LoadedBallBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_angular_contact_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "LoadedAngularContactThrustBallBearingElement":
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
class LoadedAngularContactThrustBallBearingElement(
    _2190.LoadedAngularContactBallBearingElement
):
    """LoadedAngularContactThrustBallBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_ANGULAR_CONTACT_THRUST_BALL_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedAngularContactThrustBallBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedAngularContactThrustBallBearingElement
        """
        return _Cast_LoadedAngularContactThrustBallBearingElement(self)
