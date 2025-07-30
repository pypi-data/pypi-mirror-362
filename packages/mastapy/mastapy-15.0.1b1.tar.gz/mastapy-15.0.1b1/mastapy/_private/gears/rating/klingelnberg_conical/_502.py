"""KlingelnbergCycloPalloidConicalGearMeshRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears.rating.conical import _630

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical",
    "KlingelnbergCycloPalloidConicalGearMeshRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.analysis import _1336
    from mastapy._private.gears.rating import _443, _451
    from mastapy._private.gears.rating.klingelnberg_hypoid import _499
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _496

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearMeshRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearMeshRating._Cast_KlingelnbergCycloPalloidConicalGearMeshRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearMeshRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearMeshRating:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearMeshRating to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearMeshRating"

    @property
    def conical_gear_mesh_rating(self: "CastSelf") -> "_630.ConicalGearMeshRating":
        return self.__parent__._cast(_630.ConicalGearMeshRating)

    @property
    def gear_mesh_rating(self: "CastSelf") -> "_451.GearMeshRating":
        from mastapy._private.gears.rating import _451

        return self.__parent__._cast(_451.GearMeshRating)

    @property
    def abstract_gear_mesh_rating(self: "CastSelf") -> "_443.AbstractGearMeshRating":
        from mastapy._private.gears.rating import _443

        return self.__parent__._cast(_443.AbstractGearMeshRating)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_496.KlingelnbergCycloPalloidSpiralBevelGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _496

        return self.__parent__._cast(
            _496.KlingelnbergCycloPalloidSpiralBevelGearMeshRating
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_mesh_rating(
        self: "CastSelf",
    ) -> "_499.KlingelnbergCycloPalloidHypoidGearMeshRating":
        from mastapy._private.gears.rating.klingelnberg_hypoid import _499

        return self.__parent__._cast(_499.KlingelnbergCycloPalloidHypoidGearMeshRating)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_mesh_rating(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearMeshRating":
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
class KlingelnbergCycloPalloidConicalGearMeshRating(_630.ConicalGearMeshRating):
    """KlingelnbergCycloPalloidConicalGearMeshRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_MESH_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearMeshRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearMeshRating
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearMeshRating(self)
