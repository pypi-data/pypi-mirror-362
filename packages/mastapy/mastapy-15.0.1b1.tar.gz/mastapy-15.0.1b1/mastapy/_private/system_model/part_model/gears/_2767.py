"""Gear"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.part_model import _2693

_GEAR = python_net_import("SMT.MastaAPI.SystemModel.PartModel.Gears", "Gear")

if TYPE_CHECKING:
    from typing import Any, Optional, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051
    from mastapy._private.system_model import _2414
    from mastapy._private.system_model.part_model import _2670, _2698
    from mastapy._private.system_model.part_model.gears import (
        _2750,
        _2752,
        _2754,
        _2755,
        _2756,
        _2758,
        _2760,
        _2762,
        _2764,
        _2765,
        _2769,
        _2771,
        _2773,
        _2775,
        _2777,
        _2781,
        _2783,
        _2785,
        _2787,
        _2788,
        _2789,
        _2791,
    )
    from mastapy._private.system_model.part_model.shaft_model import _2714

    Self = TypeVar("Self", bound="Gear")
    CastSelf = TypeVar("CastSelf", bound="Gear._Cast_Gear")


__docformat__ = "restructuredtext en"
__all__ = ("Gear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_Gear:
    """Special nested class for casting Gear to subclasses."""

    __parent__: "Gear"

    @property
    def mountable_component(self: "CastSelf") -> "_2693.MountableComponent":
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
    def agma_gleason_conical_gear(self: "CastSelf") -> "_2750.AGMAGleasonConicalGear":
        from mastapy._private.system_model.part_model.gears import _2750

        return self.__parent__._cast(_2750.AGMAGleasonConicalGear)

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
    def concept_gear(self: "CastSelf") -> "_2758.ConceptGear":
        from mastapy._private.system_model.part_model.gears import _2758

        return self.__parent__._cast(_2758.ConceptGear)

    @property
    def conical_gear(self: "CastSelf") -> "_2760.ConicalGear":
        from mastapy._private.system_model.part_model.gears import _2760

        return self.__parent__._cast(_2760.ConicalGear)

    @property
    def cylindrical_gear(self: "CastSelf") -> "_2762.CylindricalGear":
        from mastapy._private.system_model.part_model.gears import _2762

        return self.__parent__._cast(_2762.CylindricalGear)

    @property
    def cylindrical_planet_gear(self: "CastSelf") -> "_2764.CylindricalPlanetGear":
        from mastapy._private.system_model.part_model.gears import _2764

        return self.__parent__._cast(_2764.CylindricalPlanetGear)

    @property
    def face_gear(self: "CastSelf") -> "_2765.FaceGear":
        from mastapy._private.system_model.part_model.gears import _2765

        return self.__parent__._cast(_2765.FaceGear)

    @property
    def hypoid_gear(self: "CastSelf") -> "_2771.HypoidGear":
        from mastapy._private.system_model.part_model.gears import _2771

        return self.__parent__._cast(_2771.HypoidGear)

    @property
    def klingelnberg_cyclo_palloid_conical_gear(
        self: "CastSelf",
    ) -> "_2773.KlingelnbergCycloPalloidConicalGear":
        from mastapy._private.system_model.part_model.gears import _2773

        return self.__parent__._cast(_2773.KlingelnbergCycloPalloidConicalGear)

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear(
        self: "CastSelf",
    ) -> "_2775.KlingelnbergCycloPalloidHypoidGear":
        from mastapy._private.system_model.part_model.gears import _2775

        return self.__parent__._cast(_2775.KlingelnbergCycloPalloidHypoidGear)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear(
        self: "CastSelf",
    ) -> "_2777.KlingelnbergCycloPalloidSpiralBevelGear":
        from mastapy._private.system_model.part_model.gears import _2777

        return self.__parent__._cast(_2777.KlingelnbergCycloPalloidSpiralBevelGear)

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
    def worm_gear(self: "CastSelf") -> "_2789.WormGear":
        from mastapy._private.system_model.part_model.gears import _2789

        return self.__parent__._cast(_2789.WormGear)

    @property
    def zerol_bevel_gear(self: "CastSelf") -> "_2791.ZerolBevelGear":
        from mastapy._private.system_model.part_model.gears import _2791

        return self.__parent__._cast(_2791.ZerolBevelGear)

    @property
    def gear(self: "CastSelf") -> "Gear":
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
class Gear(_2693.MountableComponent):
    """Gear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cloned_from(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClonedFrom")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def even_number_of_teeth_required(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "EvenNumberOfTeethRequired")

        if temp is None:
            return False

        return temp

    @even_number_of_teeth_required.setter
    @exception_bridge
    @enforce_parameter_types
    def even_number_of_teeth_required(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvenNumberOfTeethRequired",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def is_clone_gear(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsCloneGear")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Length")

        if temp is None:
            return 0.0

        return temp

    @length.setter
    @exception_bridge
    @enforce_parameter_types
    def length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Length", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MaximumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @maximum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def maximum_and_minimum_number_of_teeth_deviation(self: "Self") -> "Optional[int]":
        """Optional[int]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation"
        )

        if temp is None:
            return None

        return temp

    @maximum_and_minimum_number_of_teeth_deviation.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_and_minimum_number_of_teeth_deviation(
        self: "Self", value: "Optional[int]"
    ) -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumAndMinimumNumberOfTeethDeviation", value
        )

    @property
    @exception_bridge
    def minimum_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "MinimumNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @minimum_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def active_gear_design(self: "Self") -> "_1051.GearDesign":
        """mastapy.gears.gear_designs.GearDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveGearDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_2769.GearSet":
        """mastapy.system_model.part_model.gears.GearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def shaft(self: "Self") -> "_2714.Shaft":
        """mastapy.system_model.part_model.shaft_model.Shaft

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def connect_to(self: "Self", other_gear: "Gear") -> None:
        """Method does not return.

        Args:
            other_gear (mastapy.system_model.part_model.gears.Gear)
        """
        pythonnet_method_call(
            self.wrapped, "ConnectTo", other_gear.wrapped if other_gear else None
        )

    @property
    def cast_to(self: "Self") -> "_Cast_Gear":
        """Cast to another type.

        Returns:
            _Cast_Gear
        """
        return _Cast_Gear(self)
