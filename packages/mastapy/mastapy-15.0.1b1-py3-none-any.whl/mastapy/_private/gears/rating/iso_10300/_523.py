"""ISO10300SingleFlankRatingMethodB1"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.iso_10300 import _520
from mastapy._private.gears.rating.virtual_cylindrical_gears import _481

_ISO10300_SINGLE_FLANK_RATING_METHOD_B1 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRatingMethodB1"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.conical import _634

    Self = TypeVar("Self", bound="ISO10300SingleFlankRatingMethodB1")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300SingleFlankRatingMethodB1._Cast_ISO10300SingleFlankRatingMethodB1",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRatingMethodB1",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRatingMethodB1:
    """Special nested class for casting ISO10300SingleFlankRatingMethodB1 to subclasses."""

    __parent__: "ISO10300SingleFlankRatingMethodB1"

    @property
    def iso10300_single_flank_rating(
        self: "CastSelf",
    ) -> "_520.ISO10300SingleFlankRating":
        return self.__parent__._cast(_520.ISO10300SingleFlankRating)

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_634.ConicalGearSingleFlankRating":
        from mastapy._private.gears.rating.conical import _634

        return self.__parent__._cast(_634.ConicalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def iso10300_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "ISO10300SingleFlankRatingMethodB1":
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
class ISO10300SingleFlankRatingMethodB1(
    _520.ISO10300SingleFlankRating[_481.VirtualCylindricalGearISO10300MethodB1]
):
    """ISO10300SingleFlankRatingMethodB1

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING_METHOD_B1

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auxiliary_angle_for_tooth_form_and_tooth_correction_factor(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryAngleForToothFormAndToothCorrectionFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_e_for_generated_gear_coast_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesEForGeneratedGearCoastFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_e_for_generated_gear_drive_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesEForGeneratedGearDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_e_for_non_generated_gear_coast_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesEForNonGeneratedGearCoastFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_e_for_non_generated_gear_drive_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesEForNonGeneratedGearDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_g_for_coast_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryQuantitiesGForCoastSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_g_for_drive_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryQuantitiesGForDriveSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_h_for_coast_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryQuantitiesHForCoastSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_h_for_drive_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryQuantitiesHForDriveSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_theta_for_coast_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesThetaForCoastSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_quantities_theta_for_drive_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryQuantitiesThetaForDriveSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_moment_arm_for_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingMomentArmForGeneratedGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_moment_arm_for_non_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BendingMomentArmForNonGeneratedGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def la(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "La")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_application_angle_at_tooth_tip_of_virtual_cylindrical_gear_method_b1(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LoadApplicationAngleAtToothTipOfVirtualCylindricalGearMethodB1",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_value_of_root_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalValueOfRootStressMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_tooth_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtToothTip")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def notch_parameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NotchParameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_contact_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleContactStressMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_contact_stress_use_bevel_slip_factor_method_b1(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleContactStressUseBevelSlipFactorMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_tooth_root_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleToothRootStressMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_notch_sensitivity_factor_for_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeNotchSensitivityFactorForMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_stress_drop_in_notch_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeStressDropInNotchRoot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_grey_cast_iron_nitrided_and_nitro_carburized_steels_1_mum_less_than_mean_roughness_less_than_40_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForGreyCastIronNitridedAndNitroCarburizedSteels1MumLessThanMeanRoughnessLessThan40Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_grey_cast_iron_nitrided_and_nitro_carburized_steels_mean_roughness_less_than_1_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForGreyCastIronNitridedAndNitroCarburizedSteelsMeanRoughnessLessThan1Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_non_hardened_steels_1_mum_less_than_mean_roughness_less_than_40_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForNonHardenedSteels1MumLessThanMeanRoughnessLessThan40Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_non_hardened_steels_mean_roughness_less_than_1_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForNonHardenedSteelsMeanRoughnessLessThan1Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_through_hardened_and_case_hardened_steels_1_mum_less_than_mean_roughness_less_than_40_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForThroughHardenedAndCaseHardenedSteels1MumLessThanMeanRoughnessLessThan40Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_through_hardened_and_case_hardened_steels_mean_roughness_less_than_1_mum(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeSurfaceConditionFactorForThroughHardenedAndCaseHardenedSteelsMeanRoughnessLessThan1Mum",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor_for_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSurfaceConditionFactorForMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius_for_generated_gear_coast_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RootFilletRadiusForGeneratedGearCoastFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius_for_generated_gear_drive_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RootFilletRadiusForGeneratedGearDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius_for_non_generated_gear_coast_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RootFilletRadiusForNonGeneratedGearCoastFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_fillet_radius_for_non_generated_gear_drive_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RootFilletRadiusForNonGeneratedGearDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_bending_for_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorBendingForMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_contact_for_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorContactForMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_contact_use_bevel_slip_factor_for_method_b1(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SafetyFactorContactUseBevelSlipFactorForMethodB1"
        )

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
    def tooth_form_factor_for_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFormFactorForGeneratedGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_form_factor_for_non_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothFormFactorForNonGeneratedGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_for_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothRootChordalThicknessForGeneratedGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_for_non_generated_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothRootChordalThicknessForNonGeneratedGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_per_flank_for_generated_gear_coast_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothRootChordalThicknessPerFlankForGeneratedGearCoastFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_per_flank_for_generated_gear_drive_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ToothRootChordalThicknessPerFlankForGeneratedGearDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_per_flank_for_non_generated_gear_coast_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ToothRootChordalThicknessPerFlankForNonGeneratedGearCoastFlank",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_chordal_thickness_per_flank_for_non_generated_gear_drive_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ToothRootChordalThicknessPerFlankForNonGeneratedGearDriveFlank",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootStressMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRatingMethodB1":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRatingMethodB1
        """
        return _Cast_ISO10300SingleFlankRatingMethodB1(self)
