"""ReducedCylindricalGearSetDutyCycleRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.cylindrical import _554

_REDUCED_CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ReducedCylindricalGearSetDutyCycleRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.rating import _445, _453

    Self = TypeVar("Self", bound="ReducedCylindricalGearSetDutyCycleRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ReducedCylindricalGearSetDutyCycleRating._Cast_ReducedCylindricalGearSetDutyCycleRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ReducedCylindricalGearSetDutyCycleRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ReducedCylindricalGearSetDutyCycleRating:
    """Special nested class for casting ReducedCylindricalGearSetDutyCycleRating to subclasses."""

    __parent__: "ReducedCylindricalGearSetDutyCycleRating"

    @property
    def cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_554.CylindricalGearSetDutyCycleRating":
        return self.__parent__._cast(_554.CylindricalGearSetDutyCycleRating)

    @property
    def gear_set_duty_cycle_rating(self: "CastSelf") -> "_453.GearSetDutyCycleRating":
        from mastapy._private.gears.rating import _453

        return self.__parent__._cast(_453.GearSetDutyCycleRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_445.AbstractGearSetRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def reduced_cylindrical_gear_set_duty_cycle_rating(
        self: "CastSelf",
    ) -> "ReducedCylindricalGearSetDutyCycleRating":
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
class ReducedCylindricalGearSetDutyCycleRating(_554.CylindricalGearSetDutyCycleRating):
    """ReducedCylindricalGearSetDutyCycleRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REDUCED_CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ReducedCylindricalGearSetDutyCycleRating":
        """Cast to another type.

        Returns:
            _Cast_ReducedCylindricalGearSetDutyCycleRating
        """
        return _Cast_ReducedCylindricalGearSetDutyCycleRating(self)
