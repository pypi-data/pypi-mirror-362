"""BevelGearDesign"""

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
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313

_BEVEL_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "BevelGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051, _1052
    from mastapy._private.gears.gear_designs.bevel import _1306
    from mastapy._private.gears.gear_designs.conical import _1274
    from mastapy._private.gears.gear_designs.spiral_bevel import _1073
    from mastapy._private.gears.gear_designs.straight_bevel import _1065
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1069
    from mastapy._private.gears.gear_designs.zerol_bevel import _1056

    Self = TypeVar("Self", bound="BevelGearDesign")
    CastSelf = TypeVar("CastSelf", bound="BevelGearDesign._Cast_BevelGearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearDesign:
    """Special nested class for casting BevelGearDesign to subclasses."""

    __parent__: "BevelGearDesign"

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1313.AGMAGleasonConicalGearDesign":
        return self.__parent__._cast(_1313.AGMAGleasonConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1274.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1274

        return self.__parent__._cast(_1274.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

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
    def bevel_gear_design(self: "CastSelf") -> "BevelGearDesign":
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
class BevelGearDesign(_1313.AGMAGleasonConicalGearDesign):
    """BevelGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def crown_to_cross_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrownToCrossPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DedendumAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def difference_from_ideal_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DifferenceFromIdealPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_apex_to_cross_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceApexToCrossPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width_as_percent_of_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthAsPercentOfConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def finishing_method(self: "Self") -> "_1306.FinishingMethods":
        """mastapy.gears.gear_designs.bevel.FinishingMethods"""
        temp = pythonnet_property_get(self.wrapped, "FinishingMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Bevel.FinishingMethods"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1306", "FinishingMethods"
        )(value)

    @finishing_method.setter
    @exception_bridge
    @enforce_parameter_types
    def finishing_method(self: "Self", value: "_1306.FinishingMethods") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Bevel.FinishingMethods"
        )
        pythonnet_property_set(self.wrapped, "FinishingMethod", value)

    @property
    @exception_bridge
    def front_crown_to_cross_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FrontCrownToCrossPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_slot_width_at_minimum_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSlotWidthAtMinimumBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanAddendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_chordal_addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanChordalAddendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_normal_circular_thickness_for_zero_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanNormalCircularThicknessForZeroBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_normal_circular_thickness_with_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanNormalCircularThicknessWithBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_slot_width_at_minimum_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanSlotWidthAtMinimumBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_transverse_circular_thickness_for_zero_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanTransverseCircularThicknessForZeroBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_transverse_circular_thickness_with_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanTransverseCircularThicknessWithBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_slot_width_at_minimum_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterSlotWidthAtMinimumBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_transverse_circular_thickness_for_zero_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterTransverseCircularThicknessForZeroBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_transverse_circular_thickness_with_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterTransverseCircularThicknessWithBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PitchAngle")

        if temp is None:
            return 0.0

        return temp

    @pitch_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PitchAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pitch_apex_to_boot(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchApexToBoot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_apex_to_cross_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchApexToCrossPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_apex_to_crown(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchApexToCrown")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_apex_to_front_boot(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchApexToFrontBoot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_apex_to_front_crown(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchApexToFrontCrown")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_diameter_at_wheel_outer_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchDiameterAtWheelOuterSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_apex_to_cross_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootApexToCrossPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stock_allowance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StockAllowance")

        if temp is None:
            return 0.0

        return temp

    @stock_allowance.setter
    @exception_bridge
    @enforce_parameter_types
    def stock_allowance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StockAllowance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def surface_finish(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SurfaceFinish")

        if temp is None:
            return 0.0

        return temp

    @surface_finish.setter
    @exception_bridge
    @enforce_parameter_types
    def surface_finish(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SurfaceFinish", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearDesign":
        """Cast to another type.

        Returns:
            _Cast_BevelGearDesign
        """
        return _Cast_BevelGearDesign(self)
