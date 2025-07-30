"""AGMAGleasonConicalGear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2760

_AGMA_GLEASON_CONICAL_GEAR = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2693, _2698
    from mastapy._private.system_model.part_model.gears import (
        _2752,
        _2754,
        _2755,
        _2756,
        _2767,
        _2771,
        _2781,
        _2783,
        _2785,
        _2787,
        _2788,
        _2791,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGear")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGear._Cast_AGMAGleasonConicalGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGear:
    """Special nested class for casting AGMAGleasonConicalGear to subclasses."""

    __parent__: "AGMAGleasonConicalGear"

    @property
    def conical_gear(self: "CastSelf") -> "_2760.ConicalGear":
        return self.__parent__._cast(_2760.ConicalGear)

    @property
    def gear(self: "CastSelf") -> "_2767.Gear":
        from mastapy._private.system_model.part_model.gears import _2767

        return self.__parent__._cast(_2767.Gear)

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
        from mastapy._private.system_model.part_model import _2693

        return self.__parent__._cast(_2693.MountableComponent)

    @property
    def component(self: "CastSelf") -> "_2670.Component":
        from mastapy._private.system_model.part_model import _2670

        return self.__parent__._cast(_2670.Component)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bevel_differential_gear(self: "CastSelf") -> "_2752.BevelDifferentialGear":
        from mastapy._private.system_model.part_model.gears import _2752

        return self.__parent__._cast(_2752.BevelDifferentialGear)

    @property
    def bevel_differential_planet_gear(
        self: "CastSelf",
    ) -> "_2754.BevelDifferentialPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2754

        return self.__parent__._cast(_2754.BevelDifferentialPlanetGear)

    @property
    def bevel_differential_sun_gear(
        self: "CastSelf",
    ) -> "_2755.BevelDifferentialSunGear":
        from mastapy._private.system_model.part_model.gears import _2755

        return self.__parent__._cast(_2755.BevelDifferentialSunGear)

    @property
    def bevel_gear(self: "CastSelf") -> "_2756.BevelGear":
        from mastapy._private.system_model.part_model.gears import _2756

        return self.__parent__._cast(_2756.BevelGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2771.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2771

        return self.__parent__._cast(_2771.HypoidGear)

    @property
    def spiral_bevel_gear(self: "CastSelf") -> "_2781.SpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2781

        return self.__parent__._cast(_2781.SpiralBevelGear)

    @property
    def straight_bevel_diff_gear(self: "CastSelf") -> "_2783.StraightBevelDiffGear":
        from mastapy._private.system_model.part_model.gears import _2783

        return self.__parent__._cast(_2783.StraightBevelDiffGear)

    @property
    def straight_bevel_gear(self: "CastSelf") -> "_2785.StraightBevelGear":
        from mastapy._private.system_model.part_model.gears import _2785

        return self.__parent__._cast(_2785.StraightBevelGear)

    @property
    def straight_bevel_planet_gear(self: "CastSelf") -> "_2787.StraightBevelPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2787

        return self.__parent__._cast(_2787.StraightBevelPlanetGear)

    @property
    def straight_bevel_sun_gear(self: "CastSelf") -> "_2788.StraightBevelSunGear":
        from mastapy._private.system_model.part_model.gears import _2788

        return self.__parent__._cast(_2788.StraightBevelSunGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2791.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2791

        return self.__parent__._cast(_2791.ZerolBevelGear)

    @property
    def agma_gleason_conical_gear(self: "CastSelf") -> "AGMAGleasonConicalGear":
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
class AGMAGleasonConicalGear(_2760.ConicalGear):
    """AGMAGleasonConicalGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGear":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGear
        """
        return _Cast_AGMAGleasonConicalGear(self)
