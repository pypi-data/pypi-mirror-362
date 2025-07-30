"""GearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1052

_GEAR_DESIGN = python_net_import("SMT.MastaAPI.Gears.GearDesigns", "GearDesign")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.fe_model import _1317
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313
    from mastapy._private.gears.gear_designs.bevel import _1300
    from mastapy._private.gears.gear_designs.concept import _1296
    from mastapy._private.gears.gear_designs.conical import _1274
    from mastapy._private.gears.gear_designs.cylindrical import _1122, _1152
    from mastapy._private.gears.gear_designs.face import _1093, _1098, _1101
    from mastapy._private.gears.gear_designs.hypoid import _1089
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1085
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1081
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1077
    from mastapy._private.gears.gear_designs.spiral_bevel import _1073
    from mastapy._private.gears.gear_designs.straight_bevel import _1065
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069
    from mastapy._private.gears.gear_designs.worm import _1060, _1061, _1064
    from mastapy._private.gears.gear_designs.zerol_bevel import _1056

    Self = TypeVar("Self", bound="GearDesign")
    CastSelf = TypeVar("CastSelf", bound="GearDesign._Cast_GearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("GearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearDesign:
    """Special nested class for casting GearDesign to subclasses."""

    __parent__: "GearDesign"

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_1056.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1056

        return self.__parent__._cast(_1056.ZerolBevelGearDesign)

    @property
    def worm_design(self: "CastSelf") -> "_1060.WormDesign":
        from mastapy._private.gears.gear_designs.worm import _1060

        return self.__parent__._cast(_1060.WormDesign)

    @property
    def worm_gear_design(self: "CastSelf") -> "_1061.WormGearDesign":
        from mastapy._private.gears.gear_designs.worm import _1061

        return self.__parent__._cast(_1061.WormGearDesign)

    @property
    def worm_wheel_design(self: "CastSelf") -> "_1064.WormWheelDesign":
        from mastapy._private.gears.gear_designs.worm import _1064

        return self.__parent__._cast(_1064.WormWheelDesign)

    @property
    def straight_bevel_gear_design(self: "CastSelf") -> "_1065.StraightBevelGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1065

        return self.__parent__._cast(_1065.StraightBevelGearDesign)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "_1069.StraightBevelDiffGearDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069

        return self.__parent__._cast(_1069.StraightBevelDiffGearDesign)

    @property
    def spiral_bevel_gear_design(self: "CastSelf") -> "_1073.SpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1073

        return self.__parent__._cast(_1073.SpiralBevelGearDesign)

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_design(
        self: "CastSelf",
    ) -> "_1077.KlingelnbergCycloPalloidSpiralBevelGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1077

        return self.__parent__._cast(
            _1077.KlingelnbergCycloPalloidSpiralBevelGearDesign
        )

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_design(
        self: "CastSelf",
    ) -> "_1081.KlingelnbergCycloPalloidHypoidGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1081

        return self.__parent__._cast(_1081.KlingelnbergCycloPalloidHypoidGearDesign)

    @property
    def klingelnberg_conical_gear_design(
        self: "CastSelf",
    ) -> "_1085.KlingelnbergConicalGearDesign":
        from mastapy._private.gears.gear_designs.klingelnberg_conical import _1085

        return self.__parent__._cast(_1085.KlingelnbergConicalGearDesign)

    @property
    def hypoid_gear_design(self: "CastSelf") -> "_1089.HypoidGearDesign":
        from mastapy._private.gears.gear_designs.hypoid import _1089

        return self.__parent__._cast(_1089.HypoidGearDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "_1093.FaceGearDesign":
        from mastapy._private.gears.gear_designs.face import _1093

        return self.__parent__._cast(_1093.FaceGearDesign)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1098.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1098

        return self.__parent__._cast(_1098.FaceGearPinionDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1101.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1101

        return self.__parent__._cast(_1101.FaceGearWheelDesign)

    @property
    def cylindrical_gear_design(self: "CastSelf") -> "_1122.CylindricalGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1122

        return self.__parent__._cast(_1122.CylindricalGearDesign)

    @property
    def cylindrical_planet_gear_design(
        self: "CastSelf",
    ) -> "_1152.CylindricalPlanetGearDesign":
        from mastapy._private.gears.gear_designs.cylindrical import _1152

        return self.__parent__._cast(_1152.CylindricalPlanetGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1274.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1274

        return self.__parent__._cast(_1274.ConicalGearDesign)

    @property
    def concept_gear_design(self: "CastSelf") -> "_1296.ConceptGearDesign":
        from mastapy._private.gears.gear_designs.concept import _1296

        return self.__parent__._cast(_1296.ConceptGearDesign)

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1300.BevelGearDesign":
        from mastapy._private.gears.gear_designs.bevel import _1300

        return self.__parent__._cast(_1300.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1313.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313

        return self.__parent__._cast(_1313.AGMAGleasonConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "GearDesign":
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
class GearDesign(_1052.GearDesignComponent):
    """GearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def absolute_shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AbsoluteShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def names_of_meshing_gears(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NamesOfMeshingGears")

        if temp is None:
            return ""

        return temp

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
    def number_of_teeth_maintaining_ratio(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfTeethMaintainingRatio")

        if temp is None:
            return 0

        return temp

    @number_of_teeth_maintaining_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_teeth_maintaining_ratio(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfTeethMaintainingRatio",
            int(value) if value is not None else 0,
        )

    @property
    @exception_bridge
    def shaft_inner_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftInnerDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftOuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tifffe_model(self: "Self") -> "_1317.GearFEModel":
        """mastapy.gears.fe_model.GearFEModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TIFFFEModel")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GearDesign":
        """Cast to another type.

        Returns:
            _Cast_GearDesign
        """
        return _Cast_GearDesign(self)
