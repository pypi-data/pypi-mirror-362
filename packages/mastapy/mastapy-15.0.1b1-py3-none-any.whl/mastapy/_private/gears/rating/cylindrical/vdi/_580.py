"""VDI2737InternalGearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_VDI2737_INTERNAL_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.VDI", "VDI2737InternalGearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical.iso6336 import _610

    Self = TypeVar("Self", bound="VDI2737InternalGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VDI2737InternalGearSingleFlankRating._Cast_VDI2737InternalGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VDI2737InternalGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VDI2737InternalGearSingleFlankRating:
    """Special nested class for casting VDI2737InternalGearSingleFlankRating to subclasses."""

    __parent__: "VDI2737InternalGearSingleFlankRating"

    @property
    def vdi2737_internal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "VDI2737InternalGearSingleFlankRating":
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
class VDI2737InternalGearSingleFlankRating(_0.APIBase):
    """VDI2737InternalGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VDI2737_INTERNAL_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def one_and_a_half_times_normal_module(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OneAndAHalfTimesNormalModule")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def factor_of_loading_zone_of_tooth_contact_fatigue_fracture(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FactorOfLoadingZoneOfToothContactFatigueFracture"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_fracture_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueFractureSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_fracture_safety_factor_with_influence_of_rim(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueFractureSafetyFactorWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_strength_with_influence_of_rim(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueStrengthWithInfluenceOfRim")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def form_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def form_factor_for_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FormFactorForCompression")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def level_of_force_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LevelOfForceApplication")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_stress_due_to_action_of_centrifugal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocalStressDueToActionOfCentrifugalForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_stress_due_to_the_rim_bending_moment_outside_of_the_zone_of_tooth_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LocalStressDueToTheRimBendingMomentOutsideOfTheZoneOfToothContact",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_fatigue_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumFatigueStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_stress_component_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanStressComponentCompression")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_stress_component_2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanStressComponent2")

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
    def nominal_stress_due_to_action_of_centrifugal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalStressDueToActionOfCentrifugalForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def notch_sensitivity_factor_for_fatigue_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NotchSensitivityFactorForFatigueStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_planets(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def overlap_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OverlapFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peakto_peak_amplitude_of_local_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeaktoPeakAmplitudeOfLocalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peakto_peak_amplitude_of_local_stress_compression(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PeaktoPeakAmplitudeOfLocalStressCompression"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peakto_peak_amplitude_of_local_stress_stiff_rim(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PeaktoPeakAmplitudeOfLocalStressStiffRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position_of_maximum_local_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionOfMaximumLocalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position_of_maximum_local_stress_due_to_bending_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PositionOfMaximumLocalStressDueToBendingMoment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position_of_maximum_local_stress_due_to_tangential_force(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PositionOfMaximumLocalStressDueToTangentialForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_force_in_transverse_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialForceInTransverseAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reversed_fatigue_strength_of_tooth_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ReversedFatigueStrengthOfToothRoot"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_against_crack_initiation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyAgainstCrackInitiation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_against_crack_initiation_with_influence_of_rim(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyAgainstCrackInitiationWithInfluenceOfRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_against_permanent_deformation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorAgainstPermanentDeformation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_against_permanent_deformation_with_influence_of_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorAgainstPermanentDeformationWithInfluenceOfRim"
        )

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
    def stress_concentration_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressConcentrationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_factor_due_to_bending_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationFactorDueToBendingMoment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_factor_due_to_compression_by_radial_force(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationFactorDueToCompressionByRadialForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_factor_due_to_tangential_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationFactorDueToTangentialForce"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_factor_due_to_tensile_stress_in_gear_rim(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationFactorDueToTensileStressInGearRim"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tangential_force_in_transverse_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialForceInTransverseAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tensile_yield_strength_exceeded(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TensileYieldStrengthExceeded")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def tip_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TipFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iso_gear_rating(
        self: "Self",
    ) -> "_610.ISO6336AbstractMetalGearSingleFlankRating":
        """mastapy.gears.rating.cylindrical.iso6336.ISO6336AbstractMetalGearSingleFlankRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISOGearRating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_VDI2737InternalGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_VDI2737InternalGearSingleFlankRating
        """
        return _Cast_VDI2737InternalGearSingleFlankRating(self)
