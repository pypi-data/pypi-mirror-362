"""AGMA2101GearSingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.cylindrical import _556

_AGMA2101_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.AGMA", "AGMA2101GearSingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455

    Self = TypeVar("Self", bound="AGMA2101GearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMA2101GearSingleFlankRating._Cast_AGMA2101GearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMA2101GearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AGMA2101GearSingleFlankRating:
    """Special nested class for casting AGMA2101GearSingleFlankRating to subclasses."""

    __parent__: "AGMA2101GearSingleFlankRating"

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def agma2101_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "AGMA2101GearSingleFlankRating":
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
class AGMA2101GearSingleFlankRating(_556.CylindricalGearSingleFlankRating):
    """AGMA2101GearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AGMA2101_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_contact_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableContactLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_transmitted_power_for_bending_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableTransmittedPowerForBendingStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_transmitted_power_for_bending_strength_at_unity_service_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AllowableTransmittedPowerForBendingStrengthAtUnityServiceFactor",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_transmitted_power_for_pitting_resistance_at_unity_service_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AllowableTransmittedPowerForPittingResistanceAtUnityServiceFactor",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_unit_load_for_bending_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AllowableUnitLoadForBendingStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def backup_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BackupRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor_j(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactorJ")

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
    def height_of_lewis_parabola(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeightOfLewisParabola")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helical_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelicalFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_angle_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixAngleFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tolerance_diameter_for_the_agma_standard(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumToleranceDiameterForTheAGMAStandard"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_tolerance_diameter_for_the_agma_standard(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumToleranceDiameterForTheAGMAStandard"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitting_resistance_power_rating(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PittingResistancePowerRating")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reliability_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reliability_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rim_thickness_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RimThicknessFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_pitch_deviation_agma(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SinglePitchDeviationAGMA")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def stress_correction_factor_agma(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCorrectionFactorAGMA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_cycle_factor_for_pitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCycleFactorForPitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tolerance_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToleranceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_form_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFormFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_thickness_at_critical_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothThicknessAtCriticalSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def unit_load_for_bending_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UnitLoadForBendingStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_AGMA2101GearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_AGMA2101GearSingleFlankRating
        """
        return _Cast_AGMA2101GearSingleFlankRating(self)
