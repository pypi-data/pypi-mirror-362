"""CylindricalGearFlankDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating import _449

_CYLINDRICAL_GEAR_FLANK_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "CylindricalGearFlankDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearFlankDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearFlankDutyCycleRating._Cast_CylindricalGearFlankDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearFlankDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearFlankDutyCycleRating:
    """Special nested class for casting CylindricalGearFlankDutyCycleRating to subclasses."""

    __parent__: "CylindricalGearFlankDutyCycleRating"

    @property
    def gear_flank_rating(self: "CastSelf") -> "_449.GearFlankRating":
        return self.__parent__._cast(_449.GearFlankRating)

    @property
    def cylindrical_gear_flank_duty_cycle_rating(
        self: "CastSelf",
    ) -> "CylindricalGearFlankDutyCycleRating":
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
class CylindricalGearFlankDutyCycleRating(_449.GearFlankRating):
    """CylindricalGearFlankDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_FLANK_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearFlankDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearFlankDutyCycleRating
        """
        return _Cast_CylindricalGearFlankDutyCycleRating(self)
