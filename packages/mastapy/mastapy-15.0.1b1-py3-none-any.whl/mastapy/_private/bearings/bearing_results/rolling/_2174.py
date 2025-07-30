"""BallBearingRaceContactGeometry"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_BALL_BEARING_RACE_CONTACT_GEOMETRY = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "BallBearingRaceContactGeometry"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BallBearingRaceContactGeometry")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BallBearingRaceContactGeometry._Cast_BallBearingRaceContactGeometry",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallBearingRaceContactGeometry",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BallBearingRaceContactGeometry:
    """Special nested class for casting BallBearingRaceContactGeometry to subclasses."""

    __parent__: "BallBearingRaceContactGeometry"

    @property
    def ball_bearing_race_contact_geometry(
        self: "CastSelf",
    ) -> "BallBearingRaceContactGeometry":
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
class BallBearingRaceContactGeometry(_0.APIBase):
    """BallBearingRaceContactGeometry

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BALL_BEARING_RACE_CONTACT_GEOMETRY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def ball_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def race_groove_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceGrooveRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def ball_centre(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BallCentre")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def race_centre(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RaceCentre")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_BallBearingRaceContactGeometry":
        """Cast to another type.

        Returns:
            _Cast_BallBearingRaceContactGeometry
        """
        return _Cast_BallBearingRaceContactGeometry(self)
