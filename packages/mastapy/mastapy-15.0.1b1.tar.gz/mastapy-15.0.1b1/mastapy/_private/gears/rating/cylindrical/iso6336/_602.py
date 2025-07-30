"""ISO63361996GearSingleFlankRating"""

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
from mastapy._private.gears.rating.cylindrical.iso6336 import _610

_ISO63361996_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ISO63361996GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.cylindrical import _556
    from mastapy._private.gears.rating.cylindrical.din3990 import _623
    from mastapy._private.gears.rating.cylindrical.iso6336 import _608

    Self = TypeVar("Self", bound="ISO63361996GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO63361996GearSingleFlankRating._Cast_ISO63361996GearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO63361996GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO63361996GearSingleFlankRating:
    """Special nested class for casting ISO63361996GearSingleFlankRating to subclasses."""

    __parent__: "ISO63361996GearSingleFlankRating"

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_610.ISO6336AbstractMetalGearSingleFlankRating":
        return self.__parent__._cast(_610.ISO6336AbstractMetalGearSingleFlankRating)

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_608.ISO6336AbstractGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _608

        return self.__parent__._cast(_608.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _556

        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def din3990_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_623.DIN3990GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _623

        return self.__parent__._cast(_623.DIN3990GearSingleFlankRating)

    @property
    def iso63361996_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO63361996GearSingleFlankRating":
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
class ISO63361996GearSingleFlankRating(_610.ISO6336AbstractMetalGearSingleFlankRating):
    """ISO63361996GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO63361996_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def nominal_tooth_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalToothRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO63361996GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO63361996GearSingleFlankRating
        """
        return _Cast_ISO63361996GearSingleFlankRating(self)
