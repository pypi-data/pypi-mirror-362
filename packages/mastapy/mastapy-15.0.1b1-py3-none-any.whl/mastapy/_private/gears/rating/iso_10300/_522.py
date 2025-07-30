"""ISO10300SingleFlankRatingHypoidMethodB2"""

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

_ISO10300_SINGLE_FLANK_RATING_HYPOID_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRatingHypoidMethodB2"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.conical import _634
    from mastapy._private.gears.rating.iso_10300 import _520

    Self = TypeVar("Self", bound="ISO10300SingleFlankRatingHypoidMethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300SingleFlankRatingHypoidMethodB2._Cast_ISO10300SingleFlankRatingHypoidMethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRatingHypoidMethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRatingHypoidMethodB2:
    """Special nested class for casting ISO10300SingleFlankRatingHypoidMethodB2 to subclasses."""

    __parent__: "ISO10300SingleFlankRatingHypoidMethodB2"

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
    def iso10300_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "ISO10300SingleFlankRatingHypoidMethodB2":
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
class ISO10300SingleFlankRatingHypoidMethodB2(_524.ISO10300SingleFlankRatingMethodB2):
    """ISO10300SingleFlankRatingHypoidMethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING_HYPOID_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_centreline_and_line_from_point_of_load_application_and_fillet_point_on_pinion(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AngleBetweenCentrelineAndLineFromPointOfLoadApplicationAndFilletPointOnPinion",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_between_centreline_and_line_from_point_of_load_application_and_fillet_point_on_wheel(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AngleBetweenCentrelineAndLineFromPointOfLoadApplicationAndFilletPointOnWheel",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_value_hn1o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryValueHN1o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_value_hn2o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryValueHN2o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_shift_due_to_load_for_pinion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactShiftDueToLoadForPinion")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_shift_due_to_load_for_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactShiftDueToLoadForWheel")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_centreline_to_tool_critical_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DistanceFromCentrelineToToolCriticalCoastSideFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_centreline_to_tool_critical_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DistanceFromCentrelineToToolCriticalDriveSideFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_from_pitch_circle_to_point_of_load_application(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DistanceFromPitchCircleToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def generated_pressure_angle_of_wheel_at_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GeneratedPressureAngleOfWheelAtFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def horizontal_distance_from_centreline_to_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HorizontalDistanceFromCentrelineToFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_angle_different_between_beta_c_and_delta_alpha(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IntermediateAngleDifferentBetweenBetaCAndDeltaAlpha"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_angle_different_between_beta_d_and_delta_alpha(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IntermediateAngleDifferentBetweenBetaDAndDeltaAlpha"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_angle_beta_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateAngleBetaA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_value_g1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateValueG1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_value_eta_c(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateValueEtaC")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_value_eta_d(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateValueEtaD")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_between_centreline_and_pinion_fillet(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleBetweenCentrelineAndPinionFillet"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_centreline_to_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleFromCentrelineToFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_centreline_to_pinion_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleFromCentrelineToPinionTip"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_centreline_to_tooth_surface_at_critical_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PinionAngleFromCentrelineToToothSurfaceAtCriticalCoastSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_centreline_to_tooth_surface_at_critical_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PinionAngleFromCentrelineToToothSurfaceAtCriticalDriveSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_pitch_to_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleFromPitchToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_from_wheel_tip_to_point_of_load_application(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleFromWheelTipToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_to_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionAngleToFilletPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_angle_unbalance_between_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionAngleUnbalanceBetweenFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_difference_angle_between_tool_and_surface_at_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PinionDifferenceAngleBetweenToolAndSurfaceAtCoastSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_difference_angle_between_tool_and_surface_at_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "PinionDifferenceAngleBetweenToolAndSurfaceAtDriveSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_horizontal_distance_to_critical_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionHorizontalDistanceToCriticalFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_load_height_at_weakest_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionLoadHeightAtWeakestSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_pressure_angle_at_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionPressureAngleAtPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_radial_distance_to_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PinionRadialDistanceToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_radius_to_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionRadiusToFilletPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_tooth_strength_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionToothStrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_from_tool_centre_to_critical_pinion_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusFromToolCentreToCriticalPinionCoastSideFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_from_tool_centre_to_critical_pinion_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusFromToolCentreToCriticalPinionDriveSideFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_form_factor_for_hypoid_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothFormFactorForHypoidGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_radius_to_point_of_load_application_for_pinion(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseRadiusToPointOfLoadApplicationForPinion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_radius_to_point_of_load_application_for_wheel(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseRadiusToPointOfLoadApplicationForWheel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vertical_distance_from_pitch_circle_to_critical_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VerticalDistanceFromPitchCircleToCriticalFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vertical_distance_from_pitch_circle_to_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "VerticalDistanceFromPitchCircleToFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_centreline_and_critical_point_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleBetweenCentrelineAndCriticalPointCoastSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_centreline_and_critical_point_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleBetweenCentrelineAndCriticalPointDriveSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_centreline_and_fillet_point_on_coast_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleBetweenCentrelineAndFilletPointOnCoastSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_centreline_and_fillet_point_on_drive_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleBetweenCentrelineAndFilletPointOnDriveSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_centreline_and_pinion_fillet(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleBetweenCentrelineAndPinionFillet"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_between_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelAngleBetweenFilletPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_difference_between_path_of_action_and_tooth_surface_at_pinion_fillet(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleDifferenceBetweenPathOfActionAndToothSurfaceAtPinionFillet",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_centreline_to_tooth_surface_at_critical_fillet_point_on_coast_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleFromCentrelineToToothSurfaceAtCriticalFilletPointOnCoastSide",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_centreline_to_tooth_surface_at_critical_fillet_point_on_drive_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleFromCentrelineToToothSurfaceAtCriticalFilletPointOnDriveSide",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_pinion_tip_to_point_of_load_application(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleFromPinionTipToPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_difference_angle_between_tool_and_surface_at_coast_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelDifferenceAngleBetweenToolAndSurfaceAtCoastSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_difference_angle_between_tool_and_surface_at_drive_side_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelDifferenceAngleBetweenToolAndSurfaceAtDriveSideFilletPoint",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_horizontal_distance_from_centreline_to_critical_fillet_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelHorizontalDistanceFromCentrelineToCriticalFilletPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_load_height_at_weakest_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelLoadHeightAtWeakestSection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_radius_to_pinion_fillet_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRadiusToPinionFilletPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_rotation_through_path_of_action(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelRotationThroughPathOfAction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_tooth_strength_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelToothStrengthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h3(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H3")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h3o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H3o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h4(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H4")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h4o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H4o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar_3(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar3")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar_4(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar4")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar_5(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar5")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def alpha_do(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlphaDo")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mu_d2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MuD2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mu_d(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MuD")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRatingHypoidMethodB2":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRatingHypoidMethodB2
        """
        return _Cast_ISO10300SingleFlankRatingHypoidMethodB2(self)
