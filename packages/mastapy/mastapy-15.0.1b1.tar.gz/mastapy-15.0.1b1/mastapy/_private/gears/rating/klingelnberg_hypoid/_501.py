"""KlingelnbergCycloPalloidHypoidGearSetRating"""

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
from mastapy._private.gears.rating.klingelnberg_conical import _504

_KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergHypoid",
    "KlingelnbergCycloPalloidHypoidGearSetRating",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.analysis import _1337
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1083
    from mastapy._private.gears.rating import _445, _454
    from mastapy._private.gears.rating.conical import _633
    from mastapy._private.gears.rating.klingelnberg_hypoid import _499, _500

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidHypoidGearSetRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidHypoidGearSetRating._Cast_KlingelnbergCycloPalloidHypoidGearSetRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidHypoidGearSetRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidHypoidGearSetRating:
    """Special nested class for casting KlingelnbergCycloPalloidHypoidGearSetRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidHypoidGearSetRating"

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set_rating(
        self: "CastSelf",
    ) -> "_504.KlingelnbergCycloPalloidConicalGearSetRating":
        return self.__parent__._cast(_504.KlingelnbergCycloPalloidConicalGearSetRating)

    @property
    def conical_gear_set_rating(self: "CastSelf") -> "_633.ConicalGearSetRating":
        from mastapy._private.gears.rating.conical import _633

        return self.__parent__._cast(_633.ConicalGearSetRating)

    @property
    def gear_set_rating(self: "CastSelf") -> "_454.GearSetRating":
        from mastapy._private.gears.rating import _454

        return self.__parent__._cast(_454.GearSetRating)

    @property
    def abstract_gear_set_rating(self: "CastSelf") -> "_445.AbstractGearSetRating":
        from mastapy._private.gears.rating import _445

        return self.__parent__._cast(_445.AbstractGearSetRating)

    @property
    def abstract_gear_set_analysis(self: "CastSelf") -> "_1337.AbstractGearSetAnalysis":
        from mastapy._private.gears.analysis import _1337

        return self.__parent__._cast(_1337.AbstractGearSetAnalysis)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidHypoidGearSetRating":
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
class KlingelnbergCycloPalloidHypoidGearSetRating(
    _504.KlingelnbergCycloPalloidConicalGearSetRating
):
    """KlingelnbergCycloPalloidHypoidGearSetRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_HYPOID_GEAR_SET_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "Self",
    ) -> "_1083.KlingelnbergCycloPalloidHypoidGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearSet"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_gear_ratings(
        self: "Self",
    ) -> "List[_500.KlingelnbergCycloPalloidHypoidGearRating]":
        """List[mastapy.gears.rating.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidGearRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def klingelnberg_cyclo_palloid_hypoid_mesh_ratings(
        self: "Self",
    ) -> "List[_499.KlingelnbergCycloPalloidHypoidGearMeshRating]":
        """List[mastapy.gears.rating.klingelnberg_hypoid.KlingelnbergCycloPalloidHypoidGearMeshRating]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "KlingelnbergCycloPalloidHypoidMeshRatings"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidHypoidGearSetRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidHypoidGearSetRating
        """
        return _Cast_KlingelnbergCycloPalloidHypoidGearSetRating(self)
