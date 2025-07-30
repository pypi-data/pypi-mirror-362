"""LoadedBallBearingElement"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.bearings.bearing_results.rolling import _2222

_LOADED_BALL_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "LoadedBallBearingElement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import (
        _2174,
        _2190,
        _2193,
        _2219,
        _2223,
        _2227,
        _2243,
        _2258,
        _2261,
    )
    from mastapy._private.utility.vectors import _2037, _2038

    Self = TypeVar("Self", bound="LoadedBallBearingElement")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBallBearingElement._Cast_LoadedBallBearingElement"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBallBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBallBearingElement:
    """Special nested class for casting LoadedBallBearingElement to subclasses."""

    __parent__: "LoadedBallBearingElement"

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_angular_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2190.LoadedAngularContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2190

        return self.__parent__._cast(_2190.LoadedAngularContactBallBearingElement)

    @property
    def loaded_angular_contact_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2193.LoadedAngularContactThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2193

        return self.__parent__._cast(_2193.LoadedAngularContactThrustBallBearingElement)

    @property
    def loaded_deep_groove_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2219.LoadedDeepGrooveBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2219

        return self.__parent__._cast(_2219.LoadedDeepGrooveBallBearingElement)

    @property
    def loaded_four_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2223.LoadedFourPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2223

        return self.__parent__._cast(_2223.LoadedFourPointContactBallBearingElement)

    @property
    def loaded_multi_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2227.LoadedMultiPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2227

        return self.__parent__._cast(_2227.LoadedMultiPointContactBallBearingElement)

    @property
    def loaded_self_aligning_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2243.LoadedSelfAligningBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2243

        return self.__parent__._cast(_2243.LoadedSelfAligningBallBearingElement)

    @property
    def loaded_three_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2258.LoadedThreePointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2258

        return self.__parent__._cast(_2258.LoadedThreePointContactBallBearingElement)

    @property
    def loaded_thrust_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2261.LoadedThrustBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2261

        return self.__parent__._cast(_2261.LoadedThrustBallBearingElement)

    @property
    def loaded_ball_bearing_element(self: "CastSelf") -> "LoadedBallBearingElement":
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
class LoadedBallBearingElement(_2222.LoadedElement):
    """LoadedBallBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BALL_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_left_raceway_inside_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerLeftRacewayInsideEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_raceway_inner_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerRacewayInnerEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_raceway_left_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerRacewayLeftEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_raceway_outer_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerRacewayOuterEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_raceway_right_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerRacewayRightEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_inner_right_raceway_inside_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfInnerRightRacewayInsideEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_left_raceway_inside_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterLeftRacewayInsideEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_raceway_inner_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterRacewayInnerEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_raceway_left_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterRacewayLeftEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_raceway_outer_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterRacewayOuterEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_raceway_right_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterRacewayRightEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def arc_distance_of_outer_right_raceway_inside_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ArcDistanceOfOuterRightRacewayInsideEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def centrifugal_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CentrifugalForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_inner(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchPressureVelocityInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_outer(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchPressureVelocityOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_inner(self: "Self") -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingSpeedInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_outer(self: "Self") -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingSpeedOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_inner(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingVelocityInner")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_outer(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingVelocityOuter")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def curvature_moment_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def curvature_moment_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def depth_of_maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthOfMaximumShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def depth_of_maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthOfMaximumShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def difference_between_cage_speed_and_orbit_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DifferenceBetweenCageSpeedAndOrbitSpeed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def drag_power_loss(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DragPowerLoss")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gyroscopic_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GyroscopicMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gyroscopic_moment_about_radial_direction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GyroscopicMomentAboutRadialDirection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gyroscopic_speed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GyroscopicSpeed")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_left_race_inside_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationInnerLeftRaceInsideEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_race_inner_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationInnerRaceInnerEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_race_outer_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationInnerRaceOuterEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_right_race_inside_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "HertzianEllipseMajor2bTrackTruncationInnerRightRaceInsideEdge",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_left_race_inside_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationOuterLeftRaceInsideEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_race_inner_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationOuterRaceInnerEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_race_outer_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationOuterRaceOuterEdge"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_right_race_inside_edge(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "HertzianEllipseMajor2bTrackTruncationOuterRightRaceInsideEdge",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_ellipse_major_2b_track_truncation_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianEllipseMajor2bTrackTruncationOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianSemiMajorDimensionInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianSemiMajorDimensionOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianSemiMinorDimensionInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HertzianSemiMinorDimensionOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HydrodynamicPressureForceInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HydrodynamicPressureForceOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_smearing_intensity_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSmearingIntensityInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_smearing_intensity_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSmearingIntensityOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_contact_points(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfContactPoints")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def orbit_speed_ignoring_cage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OrbitSpeedIgnoringCage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_total(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossTotal")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_inner(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_outer(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossParallelToMajorAxisInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossParallelToMajorAxisOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossParallelToMinorAxisInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossParallelToMinorAxisOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def smallest_arc_distance_of_raceway_edge_to_hertzian_contact(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SmallestArcDistanceOfRacewayEdgeToHertzianContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def smearing_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SmearingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def spinto_roll_ratio_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpintoRollRatioInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def spinto_roll_ratio_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SpintoRollRatioOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfaceVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def track_truncation_occurring_beyond_permissible_limit(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TrackTruncationOccurringBeyondPermissibleLimit"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def worst_hertzian_ellipse_major_2b_track_truncation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstHertzianEllipseMajor2bTrackTruncation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yaw_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YawAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inner_race_contact_geometries(
        self: "Self",
    ) -> "List[_2174.BallBearingRaceContactGeometry]":
        """List[mastapy.bearings.bearing_results.rolling.BallBearingRaceContactGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceContactGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_race_contact_geometries(
        self: "Self",
    ) -> "List[_2174.BallBearingRaceContactGeometry]":
        """List[mastapy.bearings.bearing_results.rolling.BallBearingRaceContactGeometry]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceContactGeometries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBallBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedBallBearingElement
        """
        return _Cast_LoadedBallBearingElement(self)
