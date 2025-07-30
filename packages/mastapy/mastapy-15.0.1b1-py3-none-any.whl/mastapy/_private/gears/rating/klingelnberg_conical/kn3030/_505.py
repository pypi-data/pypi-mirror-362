"""KlingelnbergConicalMeshSingleFlankRating"""

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
from mastapy._private.gears.rating import _457

_KLINGELNBERG_CONICAL_MESH_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.KlingelnbergConical.KN3030",
    "KlingelnbergConicalMeshSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _509, _510
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _478

    Self = TypeVar("Self", bound="KlingelnbergConicalMeshSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="KlingelnbergConicalMeshSingleFlankRating._Cast_KlingelnbergConicalMeshSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("KlingelnbergConicalMeshSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_KlingelnbergConicalMeshSingleFlankRating:
    """Special nested class for casting KlingelnbergConicalMeshSingleFlankRating to subclasses."""

    __parent__: "KlingelnbergConicalMeshSingleFlankRating"

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def klingelnberg_cyclo_palloid_hypoid_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_509.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _509

        return self.__parent__._cast(
            _509.KlingelnbergCycloPalloidHypoidMeshSingleFlankRating
        )

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_510.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating":
        from mastapy._private.gears.rating.klingelnberg_conical.kn3030 import _510

        return self.__parent__._cast(
            _510.KlingelnbergCycloPalloidSpiralBevelMeshSingleFlankRating
        )

    @property
    def klingelnberg_conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "KlingelnbergConicalMeshSingleFlankRating":
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
class KlingelnbergConicalMeshSingleFlankRating(_457.MeshSingleFlankRating):
    """KlingelnbergConicalMeshSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _KLINGELNBERG_CONICAL_MESH_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_integral_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualIntegralTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_contact_stress_number(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableContactStressNumber")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_scuffing_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableScuffingTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def alternating_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlternatingLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bevel_gear_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bevel_gear_factor_pitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearFactorPitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor_pitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactRatioFactorPitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dynamic_viscosity_at_sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicViscosityAtSumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elasticity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helical_load_distribution_factor_scuffing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelicalLoadDistributionFactorScuffing"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_angle_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_angle_factor_pitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactorPitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_distribution_factor_longitudinal(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionFactorLongitudinal"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubrication_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubrication_speed_and_roughness_factor_product(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LubricationSpeedAndRoughnessFactorProduct"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def meshing_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def operating_oil_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OperatingOilTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_torque_of_test_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionTorqueOfTestGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rated_tangential_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatedTangentialForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating_standard_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingStandardName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def relating_factor_for_the_mass_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelatingFactorForTheMassTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def running_in_allowance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RunningInAllowance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_for_scuffing(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorForScuffing")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_meshing_factor_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleMeshingFactorPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_meshing_factor_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleMeshingFactorWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specific_line_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpecificLineLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCorrectionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sump_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumpTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tangential_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_relief_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipReliefFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def zone_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ZoneFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_cylindrical_gear_set(
        self: "Self",
    ) -> "_478.KlingelnbergVirtualCylindricalGearSet":
        """mastapy.gears.rating.virtual_cylindrical_gears.KlingelnbergVirtualCylindricalGearSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualCylindricalGearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_KlingelnbergConicalMeshSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_KlingelnbergConicalMeshSingleFlankRating
        """
        return _Cast_KlingelnbergConicalMeshSingleFlankRating(self)
