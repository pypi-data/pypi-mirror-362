"""KlingelnbergCycloPalloidConicalGearSet"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.part_model.gears import _2761

_KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Gears", "KlingelnbergCycloPalloidConicalGearSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1087
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2659, _2698, _2708
    from mastapy._private.system_model.part_model.gears import _2769, _2776, _2778

    Self = TypeVar("Self", bound="KlingelnbergCycloPalloidConicalGearSet")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergCycloPalloidConicalGearSet._Cast_KlingelnbergCycloPalloidConicalGearSet",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergCycloPalloidConicalGearSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergCycloPalloidConicalGearSet:
    """Special nested class for casting KlingelnbergCycloPalloidConicalGearSet to subclasses."""

    __parent__: "KlingelnbergCycloPalloidConicalGearSet"

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
    def klingelnberg_cyclo_palloid_conical_gear_set(
        self: "CastSelf",
    ) -> "KlingelnbergCycloPalloidConicalGearSet":
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
class KlingelnbergCycloPalloidConicalGearSet(_2761.ConicalGearSet):
    """KlingelnbergCycloPalloidConicalGearSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CYCLO_PALLOID_CONICAL_GEAR_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def conical_gear_set_design(
        self: "Self",
    ) -> "_1087.KlingelnbergConicalGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def klingelnberg_conical_gear_set_design(
        self: "Self",
    ) -> "_1087.KlingelnbergConicalGearSetDesign":
        """mastapy.gears.gear_designs.klingelnberg_conical.KlingelnbergConicalGearSetDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "KlingelnbergConicalGearSetDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergCycloPalloidConicalGearSet":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergCycloPalloidConicalGearSet
        """
        return _Cast_KlingelnbergCycloPalloidConicalGearSet(self)
