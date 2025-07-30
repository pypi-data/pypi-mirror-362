"""ISO10300SingleFlankRating"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.rating.conical import _634

_ISO10300_SINGLE_FLANK_RATING = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRating"
)

if TYPE_CHECKING:
    from typing import Any, Type

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.iso_10300 import _521, _522, _523, _524
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

    Self = TypeVar("Self", bound="ISO10300SingleFlankRating")
    CastSelf = TypeVar(
        "CastSelf", bound="ISO10300SingleFlankRating._Cast_ISO10300SingleFlankRating"
    )

T = TypeVar("T", bound="_480.VirtualCylindricalGearBasic")

__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRating",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRating:
    """Special nested class for casting ISO10300SingleFlankRating to subclasses."""

    __parent__: "ISO10300SingleFlankRating"

    @property
    def conical_gear_single_flank_rating(
        self: "CastSelf",
    ) -> "_634.ConicalGearSingleFlankRating":
        return self.__parent__._cast(_634.ConicalGearSingleFlankRating)

    @property
    def gear_single_flank_rating(self: "CastSelf") -> "_455.GearSingleFlankRating":
        from mastapy._private.gears.rating import _455

        return self.__parent__._cast(_455.GearSingleFlankRating)

    @property
    def iso10300_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_521.ISO10300SingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _521

        return self.__parent__._cast(_521.ISO10300SingleFlankRatingBevelMethodB2)

    @property
    def iso10300_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_522.ISO10300SingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _522

        return self.__parent__._cast(_522.ISO10300SingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "_523.ISO10300SingleFlankRatingMethodB1":
        from mastapy._private.gears.rating.iso_10300 import _523

        return self.__parent__._cast(_523.ISO10300SingleFlankRatingMethodB1)

    @property
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_524.ISO10300SingleFlankRatingMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _524

        return self.__parent__._cast(_524.ISO10300SingleFlankRatingMethodB2)

    @property
    def iso10300_single_flank_rating(self: "CastSelf") -> "ISO10300SingleFlankRating":
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
class ISO10300SingleFlankRating(_634.ConicalGearSingleFlankRating, Generic[T]):
    """ISO10300SingleFlankRating

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def allowable_stress_number_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowableStressNumberBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def constant_lubricant_film_factor_czl_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ConstantLubricantFilmFactorCZLMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def constant_roughness_factor_czr_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstantRoughnessFactorCZRMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def constant_speed_factor_czv_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConstantSpeedFactorCZVMethodB")

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
    def life_factor_for_root_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LifeFactorForRootStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def lubricant_factor_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricantFactorMethodB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_power(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalPower")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_tangential_force_of_bevel_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalTangentialForceOfBevelGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_tangential_speed_at_mean_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTangentialSpeedAtMeanPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def product_of_lubricant_film_influence_factors(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProductOfLubricantFilmInfluenceFactors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mass_per_unit_face_width_reference_to_line_of_action(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeMassPerUnitFaceWidthReferenceToLineOfAction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_surface_condition_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeSurfaceConditionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def roughness_factor_for_contact_stress_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RoughnessFactorForContactStressMethodB"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def single_pitch_deviation(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SinglePitchDeviation")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

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
    def size_factor_for_case_flame_induction_hardened_steels_nitrided_or_nitro_carburized_steels(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SizeFactorForCaseFlameInductionHardenedSteelsNitridedOrNitroCarburizedSteels",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_for_grey_cast_iron_and_spheroidal_cast_iron(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SizeFactorForGreyCastIronAndSpheroidalCastIron"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def size_factor_for_structural_and_through_hardened_steels_spheroidal_cast_iron_perlitic_malleable_cast_iron(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SizeFactorForStructuralAndThroughHardenedSteelsSpheroidalCastIronPerliticMalleableCastIron",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def speed_factor_method_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpeedFactorMethodB")

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
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRating":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRating
        """
        return _Cast_ISO10300SingleFlankRating(self)
