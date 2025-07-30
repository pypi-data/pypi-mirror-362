"""ISO10300SingleFlankRatingBevelMethodB2"""

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
from mastapy._private.gears.rating.iso_10300 import _524

_ISO10300_SINGLE_FLANK_RATING_BEVEL_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRatingBevelMethodB2"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.conical import _634
    from mastapy._private.gears.rating.iso_10300 import _520

    Self = TypeVar("Self", bound="ISO10300SingleFlankRatingBevelMethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300SingleFlankRatingBevelMethodB2._Cast_ISO10300SingleFlankRatingBevelMethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRatingBevelMethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRatingBevelMethodB2:
    """Special nested class for casting ISO10300SingleFlankRatingBevelMethodB2 to subclasses."""

    __parent__: "ISO10300SingleFlankRatingBevelMethodB2"

    @property
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "_524.ISO10300SingleFlankRatingMethodB2":
        return self.__parent__._cast(_524.ISO10300SingleFlankRatingMethodB2)

    @property
    def iso10300_single_flank_rating(
        self: "CastSelf",
    ) -> "_520.ISO10300SingleFlankRating":
        pass

        from mastapy._private.gears.rating.iso_10300 import _520

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
    def iso10300_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "ISO10300SingleFlankRatingBevelMethodB2":
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
class ISO10300SingleFlankRatingBevelMethodB2(_524.ISO10300SingleFlankRatingMethodB2):
    """ISO10300SingleFlankRatingBevelMethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING_BEVEL_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_tangent_of_root_fillet_at_weakest_point_and_centreline_of_tooth(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AngleBetweenTangentOfRootFilletAtWeakestPointAndCentrelineOfTooth",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def assumed_angle_in_locating_weakest_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AssumedAngleInLocatingWeakestSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_mean_section_to_point_of_load_application_for_spiral_bevel_pinions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceFromMeanSectionToPointOfLoadApplicationForSpiralBevelPinions",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_mean_section_to_point_of_load_application_for_spiral_bevel_wheels(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceFromMeanSectionToPointOfLoadApplicationForSpiralBevelWheels",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_mean_section_to_point_of_load_application_for_straight_bevel_and_zerol_bevel_gear(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceFromMeanSectionToPointOfLoadApplicationForStraightBevelAndZerolBevelGear",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def initial_guess_gf_0(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InitialGuessGf0")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def iteration_balance_value_for_tooth_form_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IterationBalanceValueForToothFormFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_height_from_critical_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadHeightFromCriticalSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_transverse_radius_to_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MeanTransverseRadiusToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_pressure_angle_at_point_of_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngleAtPointOfLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def one_half_of_angle_subtended_by_normal_circular_tooth_thickness_at_point_of_load_application(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "OneHalfOfAngleSubtendedByNormalCircularToothThicknessAtPointOfLoadApplication",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def one_half_tooth_thickness_at_critical_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OneHalfToothThicknessAtCriticalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def point_of_load_application_on_path_of_action_for_maximum_root_stress_for_spiral_bevel_pinions(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PointOfLoadApplicationOnPathOfActionForMaximumRootStressForSpiralBevelPinions",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def point_of_load_application_on_path_of_action_for_maximum_root_stress_for_spiral_bevel_wheels(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PointOfLoadApplicationOnPathOfActionForMaximumRootStressForSpiralBevelWheels",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def point_of_load_application_on_path_of_action_for_maximum_root_stress_for_straight_bevel_and_zerol_bevel_gear(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PointOfLoadApplicationOnPathOfActionForMaximumRootStressForStraightBevelAndZerolBevelGear",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_distance_from_pitch_circle_to_pinion_point_of_load_and_the_wheel_tooth_centreline(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeDistanceFromPitchCircleToPinionPointOfLoadAndTheWheelToothCentreline",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_form_factor_for_bevel_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFormFactorForBevelGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_strength_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothStrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def g0(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "G0")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gxb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gxb")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gyb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gyb")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gza(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gza")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gzb(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gzb")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def alphah(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Alphah")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRatingBevelMethodB2":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRatingBevelMethodB2
        """
        return _Cast_ISO10300SingleFlankRatingBevelMethodB2(self)
