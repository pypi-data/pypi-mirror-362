"""AGMAGleasonConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model.gears import _2761

_AGMA_GLEASON_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "AGMAGleasonConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.gears import (
        _2753,
        _2757,
        _2769,
        _2772,
        _2782,
        _2784,
        _2786,
        _2792,
    )

    Self = TypeVar("Self", bound="AGMAGleasonConicalGearSet")
    CastSelf = TypeVar(
        "CastSelf", bound="AGMAGleasonConicalGearSet._Cast_AGMAGleasonConicalGearSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMAGleasonConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMAGleasonConicalGearSet:
    """Special nested class for casting AGMAGleasonConicalGearSet to subclasses."""

    __parent__: "AGMAGleasonConicalGearSet"

    @property
    def conical_gear_set(self: "CastSelf") -> "_2761.ConicalGearSet":
        return self.__parent__._cast(_2761.ConicalGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        from mastapy._private.system_model.part_model.gears import _2769

        return self.__parent__._cast(_2769.GearSet)

    @property
    def specialised_assembly(self: "CastSelf") -> "_2708.SpecialisedAssembly":
        from mastapy._private.system_model.part_model import _2708

        return self.__parent__._cast(_2708.SpecialisedAssembly)

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
        from mastapy._private.system_model.part_model import _2659

        return self.__parent__._cast(_2659.AbstractAssembly)

    @property
    def part(self: "CastSelf") -> "_2698.Part":
        from mastapy._private.system_model.part_model import _2698

        return self.__parent__._cast(_2698.Part)

    @property
    def design_entity(self: "CastSelf") -> "_2414.DesignEntity":
        from mastapy._private.system_model import _2414

        return self.__parent__._cast(_2414.DesignEntity)

    @property
    def bevel_differential_gear_set(
        self: "CastSelf",
    ) -> "_2753.BevelDifferentialGearSet":
        from mastapy._private.system_model.part_model.gears import _2753

        return self.__parent__._cast(_2753.BevelDifferentialGearSet)

    @property
    def bevel_gear_set(self: "CastSelf") -> "_2757.BevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2757

        return self.__parent__._cast(_2757.BevelGearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2772.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2772

        return self.__parent__._cast(_2772.HypoidGearSet)

    @property
    def spiral_bevel_gear_set(self: "CastSelf") -> "_2782.SpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2782

        return self.__parent__._cast(_2782.SpiralBevelGearSet)

    @property
    def straight_bevel_diff_gear_set(
        self: "CastSelf",
    ) -> "_2784.StraightBevelDiffGearSet":
        from mastapy._private.system_model.part_model.gears import _2784

        return self.__parent__._cast(_2784.StraightBevelDiffGearSet)

    @property
    def straight_bevel_gear_set(self: "CastSelf") -> "_2786.StraightBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2786

        return self.__parent__._cast(_2786.StraightBevelGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2792.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2792

        return self.__parent__._cast(_2792.ZerolBevelGearSet)

    @property
    def agma_gleason_conical_gear_set(self: "CastSelf") -> "AGMAGleasonConicalGearSet":
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
class AGMAGleasonConicalGearSet(_2761.ConicalGearSet):
    """AGMAGleasonConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA_GLEASON_CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_AGMAGleasonConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_AGMAGleasonConicalGearSet
        """
        return _Cast_AGMAGleasonConicalGearSet(self)
