"""KlingelnbergCycloPalloidConicalGearRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _631

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical",
    "KlingelnbergCycloPalloidConicalGearRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1335
    from mastapy._private.gears.rating import _444, _452
    from mastapy._private.gears.rating.klingelnberg_hypoid import _500
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _497

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearRating._Cast_KlingelnbergCycloPalloidConicalGearRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearRating:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearRating"

    @property
    def conical_gear_rating(self: "CastSelf") -> "_631.ConicalGearRating":
        return self.__parent__._cast(_631.ConicalGearRating)

    @property
    def gear_rating(self: "CastSelf") -> "_452.GearRating":
        from mastapy._private.gears.rating import _452

        return self.__parent__._cast(_452.GearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "_444.AbstractGearRating":
        from mastapy._private.gears.rating import _444

        return self.__parent__._cast(_444.AbstractGearRating)

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        from mastapy._private.gears.analysis import _1335

        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_rating(
        self: "CastSelf",
    ) -> "_497.KlingelnbergCycloPalloidSpiralBevelGearRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _497

        return self.__parent__._cast(_497.KlingelnbergCycloPalloidSpiralBevelGearRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_rating(
        self: "CastSelf",
    ) -> "_500.KlingelnbergCycloPalloidHypoidGearRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _500

        return self.__parent__._cast(_500.KlingelnbergCycloPalloidHypoidGearRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearRating":
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
class KlingelnbergCycloPalloidConicalGearRating(_631.ConicalGearRating):
    """KlingelnbergCycloPalloidConicalGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearRating
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearRating(self)
