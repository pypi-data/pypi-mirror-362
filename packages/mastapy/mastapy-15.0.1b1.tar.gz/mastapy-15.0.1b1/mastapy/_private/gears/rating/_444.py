"""AbstractGearRating"""

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
from mastapy._private.gears.analysis import _1335

_ABSTRACT_GEAR_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "AbstractGearRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _448, _452
    from mastapy._private.gears.rating.agma_gleason_conical import _657
    from mastapy._private.gears.rating.bevel import _646
    from mastapy._private.gears.rating.concept import _639, _642
    from mastapy._private.gears.rating.conical import _629, _631
    from mastapy._private.gears.rating.cylindrical import _546, _551
    from mastapy._private.gears.rating.face import _536, _539
    from mastapy._private.gears.rating.hypoid import _530
    from mastapy._private.gears.rating.klingelnberg_conical import _503
    from mastapy._private.gears.rating.klingelnberg_hypoid import _500
    from mastapy._private.gears.rating.klingelnberg_spiral_bevel import _497
    from mastapy._private.gears.rating.spiral_bevel import _494
    from mastapy._private.gears.rating.straight_bevel import _487
    from mastapy._private.gears.rating.straight_bevel_diff import _490
    from mastapy._private.gears.rating.worm import _463, _465
    from mastapy._private.gears.rating.zerol_bevel import _461

    Self = TypeVar("Self", bound="AbstractGearRating")
    CastSelf = TypeVar("CastSelf", bound="AbstractGearRating._Cast_AbstractGearRating")


__docformat__ = "restructuredtext en"
__all__ = ("AbstractGearRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AbstractGearRating:
    """Special nested class for casting AbstractGearRating to subclasses."""

    __parent__: "AbstractGearRating"

    @property
    def abstract_gear_analysis(self: "CastSelf") -> "_1335.AbstractGearAnalysis":
        return self.__parent__._cast(_1335.AbstractGearAnalysis)

    @property
    def gear_duty_cycle_rating(self: "CastSelf") -> "_448.GearDutyCycleRating":
        from mastapy._private.gears.rating import _448

        return self.__parent__._cast(_448.GearDutyCycleRating)

    @property
    def gear_rating(self: "CastSelf") -> "_452.GearRating":
        from mastapy._private.gears.rating import _452

        return self.__parent__._cast(_452.GearRating)

    @property
    def zerol_bevel_gear_rating(self: "CastSelf") -> "_461.ZerolBevelGearRating":
        from mastapy._private.gears.rating.zerol_bevel import _461

        return self.__parent__._cast(_461.ZerolBevelGearRating)

    @property
    def worm_gear_duty_cycle_rating(self: "CastSelf") -> "_463.WormGearDutyCycleRating":
        from mastapy._private.gears.rating.worm import _463

        return self.__parent__._cast(_463.WormGearDutyCycleRating)

    @property
    def worm_gear_rating(self: "CastSelf") -> "_465.WormGearRating":
        from mastapy._private.gears.rating.worm import _465

        return self.__parent__._cast(_465.WormGearRating)

    @property
    def straight_bevel_gear_rating(self: "CastSelf") -> "_487.StraightBevelGearRating":
        from mastapy._private.gears.rating.straight_bevel import _487

        return self.__parent__._cast(_487.StraightBevelGearRating)

    @property
    def straight_bevel_diff_gear_rating(
        self: "CastSelf",
    ) -> "_490.StraightBevelDiffGearRating":
        from mastapy._private.gears.rating.straight_bevel_diff import _490

        return self.__parent__._cast(_490.StraightBevelDiffGearRating)

    @property
    def spiral_bevel_gear_rating(self: "CastSelf") -> "_494.SpiralBevelGearRating":
        from mastapy._private.gears.rating.spiral_bevel import _494

        return self.__parent__._cast(_494.SpiralBevelGearRating)

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
    ) -> "_503.KlingelnbergCycloPalloidConicalGearRating":
        from mastapy._private.gears.rating.klingelnberg_conical import _503

        return self.__parent__._cast(_503.KlingelnbergCycloPalloidConicalGearRating)

    @property
    def hypoid_gear_rating(self: "CastSelf") -> "_530.HypoidGearRating":
        from mastapy._private.gears.rating.hypoid import _530

        return self.__parent__._cast(_530.HypoidGearRating)

    @property
    def face_gear_duty_cycle_rating(self: "CastSelf") -> "_536.FaceGearDutyCycleRating":
        from mastapy._private.gears.rating.face import _536

        return self.__parent__._cast(_536.FaceGearDutyCycleRating)

    @property
    def face_gear_rating(self: "CastSelf") -> "_539.FaceGearRating":
        from mastapy._private.gears.rating.face import _539

        return self.__parent__._cast(_539.FaceGearRating)

    @property
    def cylindrical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_546.CylindricalGearDutyCycleRating":
        from mastapy._private.gears.rating.cylindrical import _546

        return self.__parent__._cast(_546.CylindricalGearDutyCycleRating)

    @property
    def cylindrical_gear_rating(self: "CastSelf") -> "_551.CylindricalGearRating":
        from mastapy._private.gears.rating.cylindrical import _551

        return self.__parent__._cast(_551.CylindricalGearRating)

    @property
    def conical_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_629.ConicalGearDutyCycleRating":
        from mastapy._private.gears.rating.conical import _629

        return self.__parent__._cast(_629.ConicalGearDutyCycleRating)

    @property
    def conical_gear_rating(self: "CastSelf") -> "_631.ConicalGearRating":
        from mastapy._private.gears.rating.conical import _631

        return self.__parent__._cast(_631.ConicalGearRating)

    @property
    def concept_gear_duty_cycle_rating(
        self: "CastSelf",
    ) -> "_639.ConceptGearDutyCycleRating":
        from mastapy._private.gears.rating.concept import _639

        return self.__parent__._cast(_639.ConceptGearDutyCycleRating)

    @property
    def concept_gear_rating(self: "CastSelf") -> "_642.ConceptGearRating":
        from mastapy._private.gears.rating.concept import _642

        return self.__parent__._cast(_642.ConceptGearRating)

    @property
    def bevel_gear_rating(self: "CastSelf") -> "_646.BevelGearRating":
        from mastapy._private.gears.rating.bevel import _646

        return self.__parent__._cast(_646.BevelGearRating)

    @property
    def agma_gleason_conical_gear_rating(
        self: "CastSelf",
    ) -> "_657.AGMAGleasonConicalGearRating":
        from mastapy._private.gears.rating.agma_gleason_conical import _657

        return self.__parent__._cast(_657.AGMAGleasonConicalGearRating)

    @property
    def abstract_gear_rating(self: "CastSelf") -> "AbstractGearRating":
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
class AbstractGearRating(_1335.AbstractGearAnalysis):
    """AbstractGearRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ABSTRACT_GEAR_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cycles_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cycles_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cycles_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclesToFailContact")

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
    def gear_reliability_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_reliability_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearReliabilityContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_bending_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_bending_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedBendingSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_contact_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForFatigue"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_contact_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NormalisedContactSafetyFactorForStatic"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_safety_factor_for_fatigue(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForFatigue")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_safety_factor_for_static(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedSafetyFactorForStatic")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_to_fail(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFail")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_to_fail_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def time_to_fail_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TimeToFailContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_gear_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalGearReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AbstractGearRating":
        """Cast to another type.

        Returns:
            _Cast_AbstractGearRating
        """
        return _Cast_AbstractGearRating(self)
