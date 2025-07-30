"""KlingelnbergCycloPalloidHypoidGearSingleFlankRating"""

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
from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _507

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030",
    "KlingelnbergCycloPalloidHypoidGearSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSingleFlankRating._Cast_KlingelnbergCycloPalloidHypoidGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSingleFlankRating:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSingleFlankRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSingleFlankRating"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_507.KlingelnbergCycloPalloidConicalGearSingleFlankRating":
        return self.__parent__._cast(
            _507.KlingelnbergCycloPalloidConicalGearSingleFlankRating
        )

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSingleFlankRating":
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
class KlingelnbergCycloPalloidHypoidGearSingleFlankRating(
    _507.KlingelnbergCycloPalloidConicalGearSingleFlankRating
):
    """KlingelnbergCycloPalloidHypoidGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def tangential_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_KlingelnbergCycloPalloidHypoidGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSingleFlankRating
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSingleFlankRating(self)
