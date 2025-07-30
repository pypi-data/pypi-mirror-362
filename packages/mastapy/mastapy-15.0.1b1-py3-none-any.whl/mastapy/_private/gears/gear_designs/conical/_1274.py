"""ConicalGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1051

_CONICAL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _423
    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313
    from mastapy._private.gears.gear_designs.bevel import _1300
    from mastapy._private.gears.gear_designs.cylindrical import _1191
    from mastapy._private.gears.gear_designs.hypoid import _1089
    from mastapy._private.gears.gear_designs.klingelnberg_conical import _1085
    from mastapy._private.gears.gear_designs.klingelnberg_hypoid import _1081
    from mastapy._private.gears.gear_designs.klingelnberg_spiral_bevel import _1077
    from mastapy._private.gears.gear_designs.spiral_bevel import _1073
    from mastapy._private.gears.gear_designs.straight_bevel import _1065
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069
    from mastapy._private.gears.gear_designs.zerol_bevel import _1056
    from mastapy._private.gears.manufacturing.bevel import _899

    Self = TypeVar("Self", bound="ConicalGearDesign")
    CastSelf = TypeVar("CastSelf", bound="ConicalGearDesign._Cast_ConicalGearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalGearDesign:
    """Special nested class for casting ConicalGearDesign to subclasses."""

    __parent__: "ConicalGearDesign"

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_gear_design(self: "CastSelf") -> "_1056.ZerolBevelGearDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1056

        return self.__parent__._cast(_1056.ZerolBevelGearDesign)

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
    def conical_gear_design(self: "CastSelf") -> "ConicalGearDesign":
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
class ConicalGearDesign(_1051.GearDesign):
    """ConicalGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cutter_edge_radius_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterEdgeRadiusConcave")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutter_edge_radius_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterEdgeRadiusConvex")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hand(self: "Self") -> "_423.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._423", "Hand")(
            value
        )

    @hand.setter
    @exception_bridge
    @enforce_parameter_types
    def hand(self: "Self", value: "_423.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    @exception_bridge
    def inner_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def straddle_mounted(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "StraddleMounted")

        if temp is None:
            return False

        return temp

    @straddle_mounted.setter
    @exception_bridge
    @enforce_parameter_types
    def straddle_mounted(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "StraddleMounted", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def use_cutter_tilt(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCutterTilt")

        if temp is None:
            return False

        return temp

    @use_cutter_tilt.setter
    @exception_bridge
    @enforce_parameter_types
    def use_cutter_tilt(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseCutterTilt", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def flank_measurement_border(self: "Self") -> "_899.FlankMeasurementBorder":
        """mastapy.gears.manufacturing.bevel.FlankMeasurementBorder

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankMeasurementBorder")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def surface_roughness(self: "Self") -> "_1191.SurfaceRoughness":
        """mastapy.gears.gear_designs.cylindrical.SurfaceRoughness

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceRoughness")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalGearDesign":
        """Cast to another type.

        Returns:
            _Cast_ConicalGearDesign
        """
        return _Cast_ConicalGearDesign(self)
