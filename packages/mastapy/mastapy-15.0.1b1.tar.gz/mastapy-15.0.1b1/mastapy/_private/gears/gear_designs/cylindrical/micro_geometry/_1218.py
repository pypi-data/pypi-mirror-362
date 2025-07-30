"""CylindricalGearProfileModification"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.micro_geometry import _673

_CYLINDRICAL_GEAR_PROFILE_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearProfileModification",
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import (
        _1219,
        _1242,
    )
    from mastapy._private.gears.micro_geometry import _670
    from mastapy._private.utility_gui.charts import _2070

    Self = TypeVar("Self", bound="CylindricalGearProfileModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearProfileModification._Cast_CylindricalGearProfileModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearProfileModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearProfileModification:
    """Special nested class for casting CylindricalGearProfileModification to subclasses."""

    __parent__: "CylindricalGearProfileModification"

    @property
    def profile_modification(self: "CastSelf") -> "_673.ProfileModification":
        return self.__parent__._cast(_673.ProfileModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_profile_modification_at_face_width_position(
        self: "CastSelf",
    ) -> "_1219.CylindricalGearProfileModificationAtFaceWidthPosition":
        from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1219

        return self.__parent__._cast(
            _1219.CylindricalGearProfileModificationAtFaceWidthPosition
        )

    @property
    def cylindrical_gear_profile_modification(
        self: "CastSelf",
    ) -> "CylindricalGearProfileModification":
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
class CylindricalGearProfileModification(_673.ProfileModification):
    """CylindricalGearProfileModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PROFILE_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def barrelling_peak_point_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPointDiameter")

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_peak_point_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BarrellingPeakPointDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def barrelling_peak_point_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPointRadius")

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_peak_point_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BarrellingPeakPointRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def barrelling_peak_point_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPointRollAngle")

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_peak_point_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BarrellingPeakPointRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def barrelling_peak_point_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPointRollDistance")

        if temp is None:
            return 0.0

        return temp

    @barrelling_peak_point_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def barrelling_peak_point_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BarrellingPeakPointRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimitDiameter")

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_diameter_for_zero_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitDiameterForZeroRootRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_diameter_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_diameter_for_zero_root_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitDiameterForZeroRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimitRadius")

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_radius_for_zero_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitRadiusForZeroRootRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_radius_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_radius_for_zero_root_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRadiusForZeroRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimitRollAngle")

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_roll_angle_for_zero_root_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitRollAngleForZeroRootRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_roll_angle_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_roll_angle_for_zero_root_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRollAngleForZeroRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimitRollDistance")

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_lower_limit_roll_distance_for_zero_root_relief(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitRollDistanceForZeroRootRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_lower_limit_roll_distance_for_zero_root_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_lower_limit_roll_distance_for_zero_root_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationLowerLimitRollDistanceForZeroRootRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_root_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRootReliefDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_root_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRootReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_root_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRootReliefRadius"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_root_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRootReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_root_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRootReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_root_relief_roll_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRootReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_root_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearRootReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_root_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_root_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearRootReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_tip_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearTipReliefDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_tip_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearTipReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_tip_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationOfLinearTipReliefRadius")

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_tip_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearTipReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_tip_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearTipReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_tip_relief_roll_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearTipReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_linear_tip_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfLinearTipReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_linear_tip_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_linear_tip_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfLinearTipReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_root_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRootReliefDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_root_relief_diameter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRootReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_root_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRootReliefRadius"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_root_relief_radius(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRootReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_root_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRootReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_root_relief_roll_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRootReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_root_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicRootReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_root_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_root_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicRootReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_tip_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicTipReliefDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_tip_relief_diameter(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicTipReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_tip_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicTipReliefRadius"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_tip_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicTipReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_tip_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicTipReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_tip_relief_roll_angle(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicTipReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_of_parabolic_tip_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationOfParabolicTipReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_of_parabolic_tip_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_of_parabolic_tip_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationOfParabolicTipReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimitDiameter")

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_diameter_for_zero_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitDiameterForZeroTipRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_diameter_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_diameter_for_zero_tip_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitDiameterForZeroTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimitRadius")

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_radius_for_zero_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitRadiusForZeroTipRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_radius_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_radius_for_zero_tip_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRadiusForZeroTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimitRollAngle")

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_roll_angle_for_zero_tip_relief(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitRollAngleForZeroTipRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_roll_angle_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_roll_angle_for_zero_tip_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRollAngleForZeroTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimitRollDistance")

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def evaluation_upper_limit_roll_distance_for_zero_tip_relief(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitRollDistanceForZeroTipRelief"
        )

        if temp is None:
            return 0.0

        return temp

    @evaluation_upper_limit_roll_distance_for_zero_tip_relief.setter
    @exception_bridge
    @enforce_parameter_types
    def evaluation_upper_limit_roll_distance_for_zero_tip_relief(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "EvaluationUpperLimitRollDistanceForZeroTipRelief",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief_isoagmadin(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefISOAGMADIN")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_isoagmadin.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_isoagmadin(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearReliefISOAGMADIN",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_relief_ldp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefLDP")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_ldp.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_ldp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearReliefLDP", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def linear_relief_vdi(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LinearReliefVDI")

        if temp is None:
            return 0.0

        return temp

    @linear_relief_vdi.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_relief_vdi(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "LinearReliefVDI", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pressure_angle_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleModification")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_modification_chart(self: "Self") -> "_2070.TwoDChartDefinition":
        """mastapy.utility_gui.charts.TwoDChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileModificationChart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def start_of_linear_root_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRootReliefDiameter")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_root_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRootReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_root_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRootReliefRadius")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_root_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRootReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_root_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearRootReliefRollAngle")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_root_relief_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRootReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_root_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfLinearRootReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_root_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_root_relief_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearRootReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_tip_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearTipReliefDiameter")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_tip_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearTipReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_tip_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearTipReliefRadius")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_tip_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearTipReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_tip_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfLinearTipReliefRollAngle")

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_tip_relief_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearTipReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_linear_tip_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfLinearTipReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_linear_tip_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_linear_tip_relief_roll_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfLinearTipReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_root_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfParabolicRootReliefDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_root_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRootReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_root_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicRootReliefRadius")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_root_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRootReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_root_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfParabolicRootReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_root_relief_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRootReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_root_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfParabolicRootReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_root_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_root_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicRootReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_tip_relief_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicTipReliefDiameter")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_tip_relief_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicTipReliefDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_tip_relief_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartOfParabolicTipReliefRadius")

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_tip_relief_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicTipReliefRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_tip_relief_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfParabolicTipReliefRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_tip_relief_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicTipReliefRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_parabolic_tip_relief_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "StartOfParabolicTipReliefRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @start_of_parabolic_tip_relief_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_parabolic_tip_relief_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartOfParabolicTipReliefRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def start_of_involute_check_diameter(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "StartOfInvoluteCheckDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @start_of_involute_check_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def start_of_involute_check_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "StartOfInvoluteCheckDiameter", value)

    @property
    @exception_bridge
    def use_measured_data(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseMeasuredData")

        if temp is None:
            return False

        return temp

    @use_measured_data.setter
    @exception_bridge
    @enforce_parameter_types
    def use_measured_data(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseMeasuredData", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def barrelling_peak_point(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BarrellingPeakPoint")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def evaluation_lower_limit(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EvaluationLowerLimit")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def evaluation_lower_limit_for_zero_root_relief(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationLowerLimitForZeroRootRelief"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def evaluation_upper_limit(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EvaluationUpperLimit")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def evaluation_upper_limit_for_zero_tip_relief(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EvaluationUpperLimitForZeroTipRelief"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_root_relief_evaluation(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearRootReliefEvaluation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_root_relief_start(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearRootReliefStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_tip_relief_evaluation(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearTipReliefEvaluation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def linear_tip_relief_start(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearTipReliefStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parabolic_root_relief_evaluation(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParabolicRootReliefEvaluation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parabolic_root_relief_start(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParabolicRootReliefStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parabolic_tip_relief_evaluation(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParabolicTipReliefEvaluation")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def parabolic_tip_relief_start(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParabolicTipReliefStart")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_modification_for_customer_102cad(
        self: "Self",
    ) -> "_1242.ProfileModificationForCustomer102CAD":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.ProfileModificationForCustomer102CAD

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProfileModificationForCustomer102CAD"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def start_of_involute_check(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StartOfInvoluteCheck")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def relief_of(self: "Self", roll_distance: "float") -> "float":
        """float

        Args:
            roll_distance (float)
        """
        roll_distance = float(roll_distance)
        method_result = pythonnet_method_call(
            self.wrapped, "ReliefOf", roll_distance if roll_distance else 0.0
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearProfileModification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearProfileModification
        """
        return _Cast_CylindricalGearProfileModification(self)
