"""CylindricalGearBiasModification"""

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
from mastapy._private.gears.micro_geometry import _660

_CYLINDRICAL_GEAR_BIAS_MODIFICATION = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry",
    "CylindricalGearBiasModification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.gears.micro_geometry import _670

    Self = TypeVar("Self", bound="CylindricalGearBiasModification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearBiasModification._Cast_CylindricalGearBiasModification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearBiasModification",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearBiasModification:
    """Special nested class for casting CylindricalGearBiasModification to subclasses."""

    __parent__: "CylindricalGearBiasModification"

    @property
    def bias_modification(self: "CastSelf") -> "_660.BiasModification":
        return self.__parent__._cast(_660.BiasModification)

    @property
    def modification(self: "CastSelf") -> "_670.Modification":
        from mastapy._private.gears.micro_geometry import _670

        return self.__parent__._cast(_670.Modification)

    @property
    def cylindrical_gear_bias_modification(
        self: "CastSelf",
    ) -> "CylindricalGearBiasModification":
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
class CylindricalGearBiasModification(_660.BiasModification):
    """CylindricalGearBiasModification

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_BIAS_MODIFICATION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def lead_evaluation_left_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadEvaluationLeftLimit")

        if temp is None:
            return 0.0

        return temp

    @lead_evaluation_left_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_evaluation_left_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeadEvaluationLeftLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lead_evaluation_right_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "LeadEvaluationRightLimit")

        if temp is None:
            return 0.0

        return temp

    @lead_evaluation_right_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def lead_evaluation_right_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LeadEvaluationRightLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_angle_mod_at_left_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleModAtLeftLimit")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle_mod_at_left_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle_mod_at_left_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleModAtLeftLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def pressure_angle_mod_at_right_limit(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleModAtRightLimit")

        if temp is None:
            return 0.0

        return temp

    @pressure_angle_mod_at_right_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle_mod_at_right_limit(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleModAtRightLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_lower_limit_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationLowerLimitDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_lower_limit_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimitDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_lower_limit_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationLowerLimitRadius")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_lower_limit_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimitRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_lower_limit_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationLowerLimitRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_lower_limit_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimitRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_lower_limit_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationLowerLimitRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_lower_limit_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_lower_limit_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationLowerLimitRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_upper_limit_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationUpperLimitDiameter"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_upper_limit_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimitDiameter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_upper_limit_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationUpperLimitRadius")

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_upper_limit_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimitRadius",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_upper_limit_roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationUpperLimitRollAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit_roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_upper_limit_roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimitRollAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def profile_evaluation_upper_limit_roll_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ProfileEvaluationUpperLimitRollDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @profile_evaluation_upper_limit_roll_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def profile_evaluation_upper_limit_roll_distance(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProfileEvaluationUpperLimitRollDistance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_left_limit_isoagmadin(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtLeftLimitISOAGMADIN")

        if temp is None:
            return 0.0

        return temp

    @relief_at_left_limit_isoagmadin.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_left_limit_isoagmadin(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtLeftLimitISOAGMADIN",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_left_limit_ldp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtLeftLimitLDP")

        if temp is None:
            return 0.0

        return temp

    @relief_at_left_limit_ldp.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_left_limit_ldp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtLeftLimitLDP",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_left_limit_vdi(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtLeftLimitVDI")

        if temp is None:
            return 0.0

        return temp

    @relief_at_left_limit_vdi.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_left_limit_vdi(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtLeftLimitVDI",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_right_limit_isoagmadin(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtRightLimitISOAGMADIN")

        if temp is None:
            return 0.0

        return temp

    @relief_at_right_limit_isoagmadin.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_right_limit_isoagmadin(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtRightLimitISOAGMADIN",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_right_limit_ldp(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtRightLimitLDP")

        if temp is None:
            return 0.0

        return temp

    @relief_at_right_limit_ldp.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_right_limit_ldp(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtRightLimitLDP",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relief_at_right_limit_vdi(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ReliefAtRightLimitVDI")

        if temp is None:
            return 0.0

        return temp

    @relief_at_right_limit_vdi.setter
    @exception_bridge
    @enforce_parameter_types
    def relief_at_right_limit_vdi(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReliefAtRightLimitVDI",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def zero_bias_relief(self: "Self") -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZeroBiasRelief")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_evaluation_lower_limit(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationLowerLimit")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def profile_evaluation_upper_limit(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileEvaluationUpperLimit")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @exception_bridge
    @enforce_parameter_types
    def relief_of(self: "Self", face_width: "float", roll_distance: "float") -> "float":
        """float

        Args:
            face_width (float)
            roll_distance (float)
        """
        face_width = float(face_width)
        roll_distance = float(roll_distance)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ReliefOf",
            face_width if face_width else 0.0,
            roll_distance if roll_distance else 0.0,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearBiasModification":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearBiasModification
        """
        return _Cast_CylindricalGearBiasModification(self)
