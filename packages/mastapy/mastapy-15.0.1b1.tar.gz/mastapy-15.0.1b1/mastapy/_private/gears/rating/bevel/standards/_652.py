"""SpiralBevelGearSingleFlankRating"""

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
from mastapy._private.gears.rating.conical import _634

_SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards", "SpiralBevelGearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.bevel.standards import _648, _650

    Self = TypeVar("Self", bound="SpiralBevelGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SpiralBevelGearSingleFlankRating._Cast_SpiralBevelGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelGearSingleFlankRating:
    """Special nested class for casting SpiralBevelGearSingleFlankRating to subclasses."""

    __parent__: "SpiralBevelGearSingleFlankRating"

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_634.ConicalGearSingleFlankRating":
        return self.__parent__._cast(_634.ConicalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def agma_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_648.AGMASpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _648

        return self.__parent__._cast(_648.AGMASpiralBevelGearSingleFlankRating)

    @property
    def gleason_spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_650.GleasonSpiralBevelGearSingleFlankRating":
        from mastapy._private.gears.rating.bevel.standards import _650

        return self.__parent__._cast(_650.GleasonSpiralBevelGearSingleFlankRating)

    @property
    def spiral_bevel_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "SpiralBevelGearSingleFlankRating":
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
class SpiralBevelGearSingleFlankRating(_634.ConicalGearSingleFlankRating):
    """SpiralBevelGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending_strength_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingStrengthGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def damage_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def damage_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DamageContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DistanceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def durability_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DurabilityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_j(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorJ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_condition_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def thermal_constant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThermalConstant")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelGearSingleFlankRating
        """
        return _Cast_SpiralBevelGearSingleFlankRating(self)
