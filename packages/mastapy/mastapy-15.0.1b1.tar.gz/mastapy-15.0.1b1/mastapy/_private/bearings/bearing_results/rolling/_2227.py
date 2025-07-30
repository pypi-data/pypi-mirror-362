"""LoadedMultiPointContactBallBearingElement"""

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
from mastapy._private.bearings.bearing_results.rolling import _2208

_LOADED_MULTI_POINT_CONTACT_BALL_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedMultiPointContactBallBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2222, _2223, _2258
    from mastapy._private.utility.vectors import _2037, _2038

    Self = TypeVar("Self", bound="LoadedMultiPointContactBallBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedMultiPointContactBallBearingElement._Cast_LoadedMultiPointContactBallBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedMultiPointContactBallBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedMultiPointContactBallBearingElement:
    """Special nested class for casting LoadedMultiPointContactBallBearingElement to subclasses."""

    __parent__: "LoadedMultiPointContactBallBearingElement"

    @property
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2208.LoadedBallBearingElement":
        return self.__parent__._cast(_2208.LoadedBallBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_four_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2223.LoadedFourPointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2223

        return self.__parent__._cast(_2223.LoadedFourPointContactBallBearingElement)

    @property
    def loaded_three_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2258.LoadedThreePointContactBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2258

        return self.__parent__._cast(_2258.LoadedThreePointContactBallBearingElement)

    @property
    def loaded_multi_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "LoadedMultiPointContactBallBearingElement":
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
class LoadedMultiPointContactBallBearingElement(_2208.LoadedBallBearingElement):
    """LoadedMultiPointContactBallBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_MULTI_POINT_CONTACT_BALL_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_inner_left(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchPressureVelocityInnerLeft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_inner_right(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchPressureVelocityInnerRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_inner_left(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingSpeedInnerLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_inner_right(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingSpeedInnerRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_inner_left(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingVelocityInnerLeft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_inner_right(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingVelocityInnerRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def curvature_moment_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def curvature_moment_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMajorDimensionInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMajorDimensionInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMinorDimensionInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMinorDimensionInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicPressureForceInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicPressureForceInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressInnerRight")

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
    def maximum_shear_stress_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressInnerRight")

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
    def minimum_lubricating_film_thickness_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalLoadInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalLoadInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossInnerLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossInnerRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_inner_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_inner_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_inner_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_inner_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMajorAxisInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMajorAxisInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMinorAxisInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMinorAxisInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_inner_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisInnerLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_inner_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisInnerRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedMultiPointContactBallBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedMultiPointContactBallBearingElement
        """
        return _Cast_LoadedMultiPointContactBallBearingElement(self)
