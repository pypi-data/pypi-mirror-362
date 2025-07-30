"""ISO6336AbstractMetalGearSingleFlankRating"""

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
from mastapy._private.gears.rating.cylindrical.iso6336 import _608

_ISO6336_ABSTRACT_METAL_GEAR_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336",
    "ISO6336AbstractMetalGearSingleFlankRating",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.cylindrical import _556
    from mastapy._private.gears.rating.cylindrical.din3990 import _623
    from mastapy._private.gears.rating.cylindrical.iso6336 import _602, _604, _606

    Self = TypeVar("Self", bound="ISO6336AbstractMetalGearSingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336AbstractMetalGearSingleFlankRating._Cast_ISO6336AbstractMetalGearSingleFlankRating",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336AbstractMetalGearSingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336AbstractMetalGearSingleFlankRating:
    """Special nested class for casting ISO6336AbstractMetalGearSingleFlankRating to subclasses."""

    __parent__: "ISO6336AbstractMetalGearSingleFlankRating"

    @property
    def iso6336_abstract_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_608.ISO6336AbstractGearSingleFlankRating":
        return self.__parent__._cast(_608.ISO6336AbstractGearSingleFlankRating)

    @property
    def cylindrical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_556.CylindricalGearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical import _556

        return self.__parent__._cast(_556.CylindricalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def iso63361996_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_602.ISO63361996GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _602

        return self.__parent__._cast(_602.ISO63361996GearSingleFlankRating)

    @property
    def iso63362006_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_604.ISO63362006GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _604

        return self.__parent__._cast(_604.ISO63362006GearSingleFlankRating)

    @property
    def iso63362019_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_606.ISO63362019GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.iso6336 import _606

        return self.__parent__._cast(_606.ISO63362019GearSingleFlankRating)

    @property
    def din3990_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_623.DIN3990GearSingleFlankRating":
        from mastapy._private.gears.rating.cylindrical.din3990 import _623

        return self.__parent__._cast(_623.DIN3990GearSingleFlankRating)

    @property
    def iso6336_abstract_metal_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "ISO6336AbstractMetalGearSingleFlankRating":
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
class ISO6336AbstractMetalGearSingleFlankRating(
    _608.ISO6336AbstractGearSingleFlankRating
):
    """ISO6336AbstractMetalGearSingleFlankRating

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_ABSTRACT_METAL_GEAR_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_pitch_deviation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasePitchDeviation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def life_factor_for_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_for_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_for_reference_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeFactorForReferenceBendingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_for_reference_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LifeFactorForReferenceContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_for_static_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForStaticBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def life_factor_for_static_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForStaticContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorForReferenceStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorForStaticStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moment_of_inertia_per_unit_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentOfInertiaPerUnitFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def profile_form_deviation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProfileFormDeviation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def relative_individual_gear_mass_per_unit_face_width_referenced_to_line_of_action(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeIndividualGearMassPerUnitFaceWidthReferencedToLineOfAction",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_notch_sensitivity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeNotchSensitivityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_notch_sensitivity_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeNotchSensitivityFactorForReferenceStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_notch_sensitivity_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeNotchSensitivityFactorForStaticStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeSurfaceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSurfaceFactorForReferenceStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSurfaceFactorForStaticStress"
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
    def roughness_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactorForReferenceStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RoughnessFactorForStaticStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shot_peening_bending_stress_benefit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShotPeeningBendingStressBenefit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_pair_tooth_contact_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SinglePairToothContactFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def size_factor_tooth_root(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorToothRoot")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def size_factor_for_reference_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SizeFactorForReferenceBendingStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_for_reference_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SizeFactorForReferenceContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SizeFactorForStaticStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_size_factor_tooth_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSizeFactorToothRoot")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def velocity_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def velocity_factor_for_reference_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityFactorForReferenceStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def velocity_factor_for_static_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VelocityFactorForStaticStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def work_hardening_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkHardeningFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336AbstractMetalGearSingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO6336AbstractMetalGearSingleFlankRating
        """
        return _Cast_ISO6336AbstractMetalGearSingleFlankRating(self)
