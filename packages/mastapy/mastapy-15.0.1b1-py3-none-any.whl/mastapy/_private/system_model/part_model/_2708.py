"""SpecialisedAssembly"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.system_model.part_model import _2659

_SPECIALISED_ASSEMBLY = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "SpecialisedAssembly"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2668, _2681, _2692, _2698
    from mastapy._private.system_model.part_model.couplings import (
        _2815,
        _2817,
        _2820,
        _2823,
        _2826,
        _2828,
        _2839,
        _2846,
        _2848,
        _2853,
    )
    from mastapy._private.system_model.part_model.cycloidal import _2806
    from mastapy._private.system_model.part_model.gears import (
        _2751,
        _2753,
        _2757,
        _2759,
        _2761,
        _2763,
        _2766,
        _2769,
        _2772,
        _2774,
        _2776,
        _2778,
        _2779,
        _2782,
        _2784,
        _2786,
        _2790,
        _2792,
    )

    Self = TypeVar("Self", bound="SpecialisedAssembly")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecialisedAssembly._Cast_SpecialisedAssembly"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecialisedAssembly",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpecialisedAssembly:
    """Special nested class for casting SpecialisedAssembly to subclasses."""

    __parent__: "SpecialisedAssembly"

    @property
    def abstract_assembly(self: "CastSelf") -> "_2659.AbstractAssembly":
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
    def bolted_joint(self: "CastSelf") -> "_2668.BoltedJoint":
        from mastapy._private.system_model.part_model import _2668

        return self.__parent__._cast(_2668.BoltedJoint)

    @property
    def flexible_pin_assembly(self: "CastSelf") -> "_2681.FlexiblePinAssembly":
        from mastapy._private.system_model.part_model import _2681

        return self.__parent__._cast(_2681.FlexiblePinAssembly)

    @property
    def microphone_array(self: "CastSelf") -> "_2692.MicrophoneArray":
        from mastapy._private.system_model.part_model import _2692

        return self.__parent__._cast(_2692.MicrophoneArray)

    @property
    def agma_gleason_conical_gear_set(
        self: "CastSelf",
    ) -> "_2751.AGMAGleasonConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2751

        return self.__parent__._cast(_2751.AGMAGleasonConicalGearSet)

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
    def concept_gear_set(self: "CastSelf") -> "_2759.ConceptGearSet":
        from mastapy._private.system_model.part_model.gears import _2759

        return self.__parent__._cast(_2759.ConceptGearSet)

    @property
    def conical_gear_set(self: "CastSelf") -> "_2761.ConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2761

        return self.__parent__._cast(_2761.ConicalGearSet)

    @property
    def cylindrical_gear_set(self: "CastSelf") -> "_2763.CylindricalGearSet":
        from mastapy._private.system_model.part_model.gears import _2763

        return self.__parent__._cast(_2763.CylindricalGearSet)

    @property
    def face_gear_set(self: "CastSelf") -> "_2766.FaceGearSet":
        from mastapy._private.system_model.part_model.gears import _2766

        return self.__parent__._cast(_2766.FaceGearSet)

    @property
    def gear_set(self: "CastSelf") -> "_2769.GearSet":
        from mastapy._private.system_model.part_model.gears import _2769

        return self.__parent__._cast(_2769.GearSet)

    @property
    def hypoid_gear_set(self: "CastSelf") -> "_2772.HypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2772

        return self.__parent__._cast(_2772.HypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "_2774.KlingelnbergCycloPalloidConicalGearSet":
        from mastapy._private.system_model.part_model.gears import _2774

        return self.__parent__._cast(_2774.KlingelnbergCycloPalloidConicalGearSet)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_set(
        self: "CastSelf",
    ) -> "_2776.KlingelnbergCycloPalloidHypoidGearSet":
        from mastapy._private.system_model.part_model.gears import _2776

        return self.__parent__._cast(_2776.KlingelnbergCycloPalloidHypoidGearSet)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_set(
        self: "CastSelf",
    ) -> "_2778.KlingelnbergCycloPalloidSpiralBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2778

        return self.__parent__._cast(_2778.KlingelnbergCycloPalloidSpiralBevelGearSet)

    @property
    def planetary_gear_set(self: "CastSelf") -> "_2779.PlanetaryGearSet":
        from mastapy._private.system_model.part_model.gears import _2779

        return self.__parent__._cast(_2779.PlanetaryGearSet)

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
    def worm_gear_set(self: "CastSelf") -> "_2790.WormGearSet":
        from mastapy._private.system_model.part_model.gears import _2790

        return self.__parent__._cast(_2790.WormGearSet)

    @property
    def zerol_bevel_gear_set(self: "CastSelf") -> "_2792.ZerolBevelGearSet":
        from mastapy._private.system_model.part_model.gears import _2792

        return self.__parent__._cast(_2792.ZerolBevelGearSet)

    @property
    def cycloidal_assembly(self: "CastSelf") -> "_2806.CycloidalAssembly":
        from mastapy._private.system_model.part_model.cycloidal import _2806

        return self.__parent__._cast(_2806.CycloidalAssembly)

    @property
    def belt_drive(self: "CastSelf") -> "_2815.BeltDrive":
        from mastapy._private.system_model.part_model.couplings import _2815

        return self.__parent__._cast(_2815.BeltDrive)

    @property
    def clutch(self: "CastSelf") -> "_2817.Clutch":
        from mastapy._private.system_model.part_model.couplings import _2817

        return self.__parent__._cast(_2817.Clutch)

    @property
    def concept_coupling(self: "CastSelf") -> "_2820.ConceptCoupling":
        from mastapy._private.system_model.part_model.couplings import _2820

        return self.__parent__._cast(_2820.ConceptCoupling)

    @property
    def coupling(self: "CastSelf") -> "_2823.Coupling":
        from mastapy._private.system_model.part_model.couplings import _2823

        return self.__parent__._cast(_2823.Coupling)

    @property
    def cvt(self: "CastSelf") -> "_2826.CVT":
        from mastapy._private.system_model.part_model.couplings import _2826

        return self.__parent__._cast(_2826.CVT)

    @property
    def part_to_part_shear_coupling(
        self: "CastSelf",
    ) -> "_2828.PartToPartShearCoupling":
        from mastapy._private.system_model.part_model.couplings import _2828

        return self.__parent__._cast(_2828.PartToPartShearCoupling)

    @property
    def rolling_ring_assembly(self: "CastSelf") -> "_2839.RollingRingAssembly":
        from mastapy._private.system_model.part_model.couplings import _2839

        return self.__parent__._cast(_2839.RollingRingAssembly)

    @property
    def spring_damper(self: "CastSelf") -> "_2846.SpringDamper":
        from mastapy._private.system_model.part_model.couplings import _2846

        return self.__parent__._cast(_2846.SpringDamper)

    @property
    def synchroniser(self: "CastSelf") -> "_2848.Synchroniser":
        from mastapy._private.system_model.part_model.couplings import _2848

        return self.__parent__._cast(_2848.Synchroniser)

    @property
    def torque_converter(self: "CastSelf") -> "_2853.TorqueConverter":
        from mastapy._private.system_model.part_model.couplings import _2853

        return self.__parent__._cast(_2853.TorqueConverter)

    @property
    def specialised_assembly(self: "CastSelf") -> "SpecialisedAssembly":
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
class SpecialisedAssembly(_2659.AbstractAssembly):
    """SpecialisedAssembly

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPECIALISED_ASSEMBLY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_SpecialisedAssembly":
        """Cast to another type.

        Returns:
            _Cast_SpecialisedAssembly
        """
        return _Cast_SpecialisedAssembly(self)
