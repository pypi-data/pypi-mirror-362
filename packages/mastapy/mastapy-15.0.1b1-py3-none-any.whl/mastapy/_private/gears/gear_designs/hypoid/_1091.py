"""HypoidGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs.agma_gleason_conical import _1315

_HYPOID_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Hypoid", "HypoidGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs import _1052, _1054
    from mastapy._private.gears.gear_designs.conical import _1276
    from mastapy._private.gears.gear_designs.hypoid import _1089, _1090

    Self = TypeVar("Self", bound="HypoidGearSetDesign")
    CastSelf = TypeVar(
        "CastSelf", bound="HypoidGearSetDesign._Cast_HypoidGearSetDesign"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidGearSetDesign:
    """Special nested class for casting HypoidGearSetDesign to subclasses."""

    __parent__: "HypoidGearSetDesign"

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
    def hypoid_gear_set_design(self: "CastSelf") -> "HypoidGearSetDesign":
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
class HypoidGearSetDesign(_1315.AGMAGleasonConicalGearSetDesign):
    """HypoidGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AveragePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @average_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def average_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AveragePressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def backlash_allowance_max(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BacklashAllowanceMax")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def backlash_allowance_min(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BacklashAllowanceMin")

        if temp is None:
            return 0.0

        return temp

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
    def depth_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DepthFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @depth_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def depth_factor(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DepthFactor", value)

    @property
    @exception_bridge
    def desired_pinion_spiral_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DesiredPinionSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @desired_pinion_spiral_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def desired_pinion_spiral_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DesiredPinionSpiralAngle",
            float(value) if value is not None else 0.0,
        )

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
    def distance_from_midpoint_of_tooth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceFromMidpointOfTooth")

        if temp is None:
            return 0.0

        return temp

    @distance_from_midpoint_of_tooth.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_from_midpoint_of_tooth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceFromMidpointOfTooth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def elastic_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_i(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorI")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hardness_ratio_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HardnessRatioFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def influence_factor_of_limit_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InfluenceFactorOfLimitPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limit_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitPressureAngle")

        if temp is None:
            return 0.0

        return temp

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
    def mean_clearance_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MeanClearanceFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @mean_clearance_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def mean_clearance_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MeanClearanceFactor", value)

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
    def modified_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @offset.setter
    @exception_bridge
    @enforce_parameter_types
    def offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Offset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pinion_concave_root_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConcaveRootPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_convex_root_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionConvexRootPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_face_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionFaceAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_inner_dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerDedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_inner_dedendum_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerDedendumLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_inner_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionInnerSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_mean_pitch_concave_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionMeanPitchConcavePressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_mean_pitch_convex_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionMeanPitchConvexPressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "PinionNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @pinion_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def pinion_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "PinionNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def pinion_offset_angle_in_pitch_plane_at_inner_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionOffsetAngleInPitchPlaneAtInnerEnd"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_offset_angle_in_pitch_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionOffsetAngleInPitchPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_offset_angle_in_root_plane(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionOffsetAngleInRootPlane")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_passed_undercut_check(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPassedUndercutCheck")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def pinion_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_root_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRootAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_thickness_modification_coefficient_backlash_included(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionThicknessModificationCoefficientBacklashIncluded"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_limit_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchLimitPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileContactRatio")

        if temp is None:
            return 0.0

        return temp

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
    def ratio_between_offset_and_wheel_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RatioBetweenOffsetAndWheelPitchDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @ratio_between_offset_and_wheel_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def ratio_between_offset_and_wheel_pitch_diameter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RatioBetweenOffsetAndWheelPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rough_cutter_point_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughCutterPointWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_angle_departure_from_perpendicular(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftAngleDepartureFromPerpendicular"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_bending(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorBending")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def specified_wheel_addendum_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedWheelAddendumAngle")

        if temp is None:
            return 0.0

        return temp

    @specified_wheel_addendum_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_wheel_addendum_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedWheelAddendumAngle",
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
    def strength_balance_obtained(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthBalanceObtained")

        if temp is None:
            return 0.0

        return temp

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
    def tooth_thickness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_number_of_teeth(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def wheel_addendum_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "WheelAddendumFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @wheel_addendum_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_addendum_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WheelAddendumFactor", value)

    @property
    @exception_bridge
    def wheel_face_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelFaceAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_face_width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @wheel_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_face_width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelFaceWidth", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_finish_cutter_point_width(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "WheelFinishCutterPointWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @wheel_finish_cutter_point_width.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_finish_cutter_point_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WheelFinishCutterPointWidth", value)

    @property
    @exception_bridge
    def wheel_finish_cutter_point_width_suppressed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "WheelFinishCutterPointWidthSuppressed"
        )

        if temp is None:
            return 0.0

        return temp

    @wheel_finish_cutter_point_width_suppressed.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_finish_cutter_point_width_suppressed(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelFinishCutterPointWidthSuppressed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_inner_blade_angle_convex(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerBladeAngleConvex")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_inner_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_inner_pitch_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelInnerPitchRadius")

        if temp is None:
            return 0.0

        return temp

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
    def wheel_inside_point_to_cross_point_along_wheel_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelInsidePointToCrossPointAlongWheelAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_mean_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelMeanWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_mean_working_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelMeanWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_number_of_teeth(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "WheelNumberOfTeeth")

        if temp is None:
            return 0

        return temp

    @wheel_number_of_teeth.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_number_of_teeth(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelNumberOfTeeth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def wheel_outer_blade_angle_concave(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelOuterBladeAngleConcave")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_outer_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelOuterSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelPitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_pitch_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @wheel_pitch_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_pitch_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "WheelPitchDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def wheel_root_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRootAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_thickness_modification_coefficient_backlash_included(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelThicknessModificationCoefficientBacklashIncluded"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_working_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelWorkingDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1089.HypoidGearDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_gears(self: "Self") -> "List[_1089.HypoidGearDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def meshes(self: "Self") -> "List[_1090.HypoidGearMeshDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Meshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def hypoid_meshes(self: "Self") -> "List[_1090.HypoidGearMeshDesign]":
        """List[mastapy.gears.gear_designs.hypoid.HypoidGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_HypoidGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_HypoidGearSetDesign
        """
        return _Cast_HypoidGearSetDesign(self)
