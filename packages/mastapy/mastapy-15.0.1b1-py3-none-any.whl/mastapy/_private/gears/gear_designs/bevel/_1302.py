"""BevelGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315
from mastapy._private.gears.gear_designs.bevel import _1310

_BEVEL_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "BevelGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears import _437
    from mastapy._private.gears.gear_designs import _1052, _1054
    from mastapy._private.gears.gear_designs.bevel import _1309, _1311
    from mastapy._private.gears.gear_designs.conical import _1271, _1276
    from mastapy._private.gears.gear_designs.spiral_bevel import _1075
    from mastapy._private.gears.gear_designs.straight_bevel import _1067
    from mastapy._private.gears.gear_designs.straight_bevel_diff import _1071
    from mastapy._private.gears.gear_designs.zerol_bevel import _1058
    from mastapy._private.math_utility import _1703

    Self = TypeVar("Self", bound="BevelGearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="BevelGearSetDesign._Cast_BevelGearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("BevelGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_BevelGearSetDesign:
    """Special nested class for casting BevelGearSetDesign to subclasses."""

    __parent__: "BevelGearSetDesign"

    @property
    def agma_gleason_conical_gear_set_design(
        self: "CastSelf",
    ) -> "_1315.AGMAGleasonConicalGearSetDesign":
        return self.__parent__._cast(_1315.AGMAGleasonConicalGearSetDesign)

    @property
    def conical_gear_set_design(self: "CastSelf") -> "_1276.ConicalGearSetDesign":
        from mastapy._private.gears.gear_designs.conical import _1276

        return self.__parent__._cast(_1276.ConicalGearSetDesign)

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        from mastapy._private.gears.gear_designs import _1054

        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def zerol_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1058.ZerolBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.zerol_bevel import _1058

        return self.__parent__._cast(_1058.ZerolBevelGearSetDesign)

    @property
    def straight_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1067.StraightBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel import _1067

        return self.__parent__._cast(_1067.StraightBevelGearSetDesign)

    @property
    def straight_bevel_diff_gear_set_design(
        self: "CastSelf",
    ) -> "_1071.StraightBevelDiffGearSetDesign":
        from mastapy._private.gears.gear_designs.straight_bevel_diff import _1071

        return self.__parent__._cast(_1071.StraightBevelDiffGearSetDesign)

    @property
    def spiral_bevel_gear_set_design(
        self: "CastSelf",
    ) -> "_1075.SpiralBevelGearSetDesign":
        from mastapy._private.gears.gear_designs.spiral_bevel import _1075

        return self.__parent__._cast(_1075.SpiralBevelGearSetDesign)

    @property
    def bevel_gear_set_design(self: "CastSelf") -> "BevelGearSetDesign":
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
class BevelGearSetDesign(_1315.AGMAGleasonConicalGearSetDesign):
    """BevelGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _BEVEL_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_scoring_index(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AllowableScoringIndex")

        if temp is None:
            return 0.0

        return temp

    @allowable_scoring_index.setter
    @exception_bridge
    @enforce_parameter_types
    def allowable_scoring_index(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AllowableScoringIndex",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def backlash_distribution_rule(self: "Self") -> "_1271.BacklashDistributionRule":
        """mastapy.gears.gear_designs.conical.BacklashDistributionRule"""
        temp = pythonnet_property_get(self.wrapped, "BacklashDistributionRule")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Conical.BacklashDistributionRule"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.conical._1271",
            "BacklashDistributionRule",
        )(value)

    @backlash_distribution_rule.setter
    @exception_bridge
    @enforce_parameter_types
    def backlash_distribution_rule(
        self: "Self", value: "_1271.BacklashDistributionRule"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Conical.BacklashDistributionRule"
        )
        pythonnet_property_set(self.wrapped, "BacklashDistributionRule", value)

    @property
    @exception_bridge
    def backlash_used_for_tooth_thickness_calculation(
        self: "Self",
    ) -> "_1703.MaxMinMean":
        """mastapy.math_utility.MaxMinMean"""
        temp = pythonnet_property_get(
            self.wrapped, "BacklashUsedForToothThicknessCalculation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.MathUtility.MaxMinMean")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.math_utility._1703", "MaxMinMean"
        )(value)

    @backlash_used_for_tooth_thickness_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def backlash_used_for_tooth_thickness_calculation(
        self: "Self", value: "_1703.MaxMinMean"
    ) -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.MathUtility.MaxMinMean")
        pythonnet_property_set(
            self.wrapped, "BacklashUsedForToothThicknessCalculation", value
        )

    @property
    @exception_bridge
    def basic_crown_gear_addendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicCrownGearAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_crown_gear_dedendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicCrownGearDedendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def circular_thickness_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CircularThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @circular_thickness_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def circular_thickness_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CircularThicknessFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def clearance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Clearance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def diametral_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DiametralPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def factor_of_safety_for_scoring(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FactorOfSafetyForScoring")

        if temp is None:
            return 0.0

        return temp

    @factor_of_safety_for_scoring.setter
    @exception_bridge
    @enforce_parameter_types
    def factor_of_safety_for_scoring(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FactorOfSafetyForScoring",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ideal_circular_thickness_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "IdealCircularThicknessFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @ideal_circular_thickness_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def ideal_circular_thickness_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IdealCircularThicknessFactor", value)

    @property
    @exception_bridge
    def ideal_pinion_mean_transverse_circular_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "IdealPinionMeanTransverseCircularThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_mean_transverse_circular_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def ideal_pinion_mean_transverse_circular_thickness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealPinionMeanTransverseCircularThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ideal_pinion_outer_transverse_circular_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "IdealPinionOuterTransverseCircularThickness"
        )

        if temp is None:
            return 0.0

        return temp

    @ideal_pinion_outer_transverse_circular_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def ideal_pinion_outer_transverse_circular_thickness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealPinionOuterTransverseCircularThickness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ideal_wheel_finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "IdealWheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_finish_cutter_point_width.setter
    @exception_bridge
    @enforce_parameter_types
    def ideal_wheel_finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealWheelFinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def ideal_wheel_mean_slot_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "IdealWheelMeanSlotWidth")

        if temp is None:
            return 0.0

        return temp

    @ideal_wheel_mean_slot_width.setter
    @exception_bridge
    @enforce_parameter_types
    def ideal_wheel_mean_slot_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IdealWheelMeanSlotWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_addendum_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_addendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_addendum_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanAddendumFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_circular_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanCircularPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_clearance_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanClearanceFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_clearance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_clearance_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MeanClearanceFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @mean_depth_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanDepthFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def mean_diametral_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDiametralPitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_working_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_number_of_teeth_for_recommended_tooth_proportions(
        self: "Self",
    ) -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumNumberOfTeethForRecommendedToothProportions"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def outer_wheel_addendum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWheelAddendum")

        if temp is None:
            return 0.0

        return temp

    @outer_wheel_addendum.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_wheel_addendum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterWheelAddendum",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_whole_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_whole_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_whole_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "OuterWholeDepth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def outer_working_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_working_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_working_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterWorkingDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngle")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PressureAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def profile_shift_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileShiftCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def round_cutter_specifications(
        self: "Self",
    ) -> "_1311.WheelFinishCutterPointWidthRestrictionMethod":
        """mastapy.gears.gear_designs.bevel.WheelFinishCutterPointWidthRestrictionMethod"""
        temp = pythonnet_property_get(self.wrapped, "RoundCutterSpecifications")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.WheelFinishCutterPointWidthRestrictionMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1311",
            "WheelFinishCutterPointWidthRestrictionMethod",
        )(value)

    @round_cutter_specifications.setter
    @exception_bridge
    @enforce_parameter_types
    def round_cutter_specifications(
        self: "Self", value: "_1311.WheelFinishCutterPointWidthRestrictionMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Bevel.WheelFinishCutterPointWidthRestrictionMethod",
        )
        pythonnet_property_set(self.wrapped, "RoundCutterSpecifications", value)

    @property
    @exception_bridge
    def specified_pinion_dedendum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedPinionDedendumAngle")

        if temp is None:
            return 0.0

        return temp

    @specified_pinion_dedendum_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_pinion_dedendum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedPinionDedendumAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_wheel_dedendum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedWheelDedendumAngle")

        if temp is None:
            return 0.0

        return temp

    @specified_wheel_dedendum_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_wheel_dedendum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedWheelDedendumAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def strength_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @strength_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def strength_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "StrengthFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def thickness_modification_coefficient_theoretical(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ThicknessModificationCoefficientTheoretical"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_proportions_input_method(
        self: "Self",
    ) -> "_1309.ToothProportionsInputMethod":
        """mastapy.gears.gear_designs.bevel.ToothProportionsInputMethod"""
        temp = pythonnet_property_get(self.wrapped, "ToothProportionsInputMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Bevel.ToothProportionsInputMethod"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1309",
            "ToothProportionsInputMethod",
        )(value)

    @tooth_proportions_input_method.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_proportions_input_method(
        self: "Self", value: "_1309.ToothProportionsInputMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Bevel.ToothProportionsInputMethod"
        )
        pythonnet_property_set(self.wrapped, "ToothProportionsInputMethod", value)

    @property
    @exception_bridge
    def tooth_taper_root_line_tilt_method(
        self: "Self",
    ) -> "_437.SpiralBevelRootLineTilt":
        """mastapy.gears.SpiralBevelRootLineTilt"""
        temp = pythonnet_property_get(self.wrapped, "ToothTaperRootLineTiltMethod")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.SpiralBevelRootLineTilt"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._437", "SpiralBevelRootLineTilt"
        )(value)

    @tooth_taper_root_line_tilt_method.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_taper_root_line_tilt_method(
        self: "Self", value: "_437.SpiralBevelRootLineTilt"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.SpiralBevelRootLineTilt"
        )
        pythonnet_property_set(self.wrapped, "ToothTaperRootLineTiltMethod", value)

    @property
    @exception_bridge
    def tooth_thickness_specification_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod":
        """EnumWithSelectedValue[mastapy.gears.gear_designs.bevel.ToothThicknessSpecificationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessSpecificationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @tooth_thickness_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_thickness_specification_method(
        self: "Self", value: "_1310.ToothThicknessSpecificationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ToothThicknessSpecificationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ToothThicknessSpecificationMethod", value)

    @property
    @exception_bridge
    def use_recommended_tooth_proportions(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseRecommendedToothProportions")

        if temp is None:
            return False

        return temp

    @use_recommended_tooth_proportions.setter
    @exception_bridge
    @enforce_parameter_types
    def use_recommended_tooth_proportions(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseRecommendedToothProportions",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def wheel_addendum_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelAddendumFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_addendum_multiplier(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelAddendumMultiplier")

        if temp is None:
            return 0.0

        return temp

    @wheel_addendum_multiplier.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_addendum_multiplier(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelAddendumMultiplier",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_finish_cutter_point_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_finish_cutter_point_width.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_finish_cutter_point_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFinishCutterPointWidth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_inner_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def whole_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WholeDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @whole_depth_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def whole_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WholeDepthFactor", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def working_depth_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WorkingDepthFactor")

        if temp is None:
            return 0.0

        return temp

    @working_depth_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def working_depth_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WorkingDepthFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mean_spiral_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MeanSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @mean_spiral_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_spiral_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MeanSpiralAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def transverse_circular_thickness_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TransverseCircularThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @transverse_circular_thickness_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def transverse_circular_thickness_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TransverseCircularThicknessFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_BevelGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_BevelGearSetDesign
        """
        return _Cast_BevelGearSetDesign(self)
