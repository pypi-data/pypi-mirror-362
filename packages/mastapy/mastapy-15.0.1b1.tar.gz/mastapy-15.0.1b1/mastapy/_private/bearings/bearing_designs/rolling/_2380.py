"""SphericalRollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.bearings.bearing_designs.rolling import _2352

_SPHERICAL_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SphericalRollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import _2372, _2375

    Self = TypeVar("Self", bound="SphericalRollerBearing")
    CastSelf = TypeVar(
        "CastSelf", bound="SphericalRollerBearing._Cast_SphericalRollerBearing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SphericalRollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SphericalRollerBearing:
    """Special nested class for casting SphericalRollerBearing to subclasses."""

    __parent__: "SphericalRollerBearing"

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2352.BarrelRollerBearing":
        return self.__parent__._cast(_2352.BarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

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
    def spherical_roller_bearing(self: "CastSelf") -> "SphericalRollerBearing":
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
class SphericalRollerBearing(_2352.BarrelRollerBearing):
    """SphericalRollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPHERICAL_ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SphericalRollerBearing":
        """Cast to another type.

        Returns:
            _Cast_SphericalRollerBearing
        """
        return _Cast_SphericalRollerBearing(self)
