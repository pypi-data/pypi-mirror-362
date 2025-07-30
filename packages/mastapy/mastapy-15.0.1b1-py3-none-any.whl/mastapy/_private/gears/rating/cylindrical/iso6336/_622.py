"""ToothFlankFractureStressStepAtAnalysisPointN1457"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private._math.vector_2d import Vector2D

_TOOTH_FLANK_FRACTURE_STRESS_STEP_AT_ANALYSIS_POINT_N1457 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ToothFlankFractureStressStepAtAnalysisPointN1457",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1135
    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="ToothFlankFractureStressStepAtAnalysisPointN1457")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureStressStepAtAnalysisPointN1457._Cast_ToothFlankFractureStressStepAtAnalysisPointN1457",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureStressStepAtAnalysisPointN1457",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureStressStepAtAnalysisPointN1457:
    """Special nested class for casting ToothFlankFractureStressStepAtAnalysisPointN1457 to subclasses."""

    __parent__: "ToothFlankFractureStressStepAtAnalysisPointN1457"

    @property
    def tooth_flank_fracture_stress_step_at_analysis_point_n1457(
        self: "CastSelf",
    ) -> "ToothFlankFractureStressStepAtAnalysisPointN1457":
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
class ToothFlankFractureStressStepAtAnalysisPointN1457(_0.APIBase):
    """ToothFlankFractureStressStepAtAnalysisPointN1457

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_STRESS_STEP_AT_ANALYSIS_POINT_N1457

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def equivalent_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_sensitivity_to_hydro_static_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueSensitivityToHydroStaticPressure"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def first_hertzian_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FirstHertzianParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def global_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GlobalNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def global_shear_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GlobalShearStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def global_transverse_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GlobalTransverseStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrostatic_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HydrostaticPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stress_due_to_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStressDueToFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_stress_due_to_normal_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalStressDueToNormalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_hertzian_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondHertzianParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def second_stress_invariant(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SecondStressInvariant")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_stress_due_to_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressDueToFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shear_stress_due_to_normal_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearStressDueToNormalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def third_normal_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThirdNormalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_stress_due_to_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseStressDueToFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_stress_due_to_normal_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransverseStressDueToNormalLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_position_on_profile(
        self: "Self",
    ) -> "_1135.CylindricalGearProfileMeasurement":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearProfileMeasurement

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPositionOnProfile")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def relative_coordinates(self: "Self") -> "Vector2D":
        """Vector2D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCoordinates")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector2d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def stress(self: "Self") -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Stress")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_ToothFlankFractureStressStepAtAnalysisPointN1457":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureStressStepAtAnalysisPointN1457
        """
        return _Cast_ToothFlankFractureStressStepAtAnalysisPointN1457(self)
