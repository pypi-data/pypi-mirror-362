"""LoadedFourPointContactBallBearingElement"""

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
from mastapy._private.bearings.bearing_results.rolling import _2227

_LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ELEMENT = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling",
    "LoadedFourPointContactBallBearingElement",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.bearings.bearing_results.rolling import _2208, _2222
    from mastapy._private.utility.vectors import _2037, _2038

    Self = TypeVar("Self", bound="LoadedFourPointContactBallBearingElement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedFourPointContactBallBearingElement._Cast_LoadedFourPointContactBallBearingElement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedFourPointContactBallBearingElement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedFourPointContactBallBearingElement:
    """Special nested class for casting LoadedFourPointContactBallBearingElement to subclasses."""

    __parent__: "LoadedFourPointContactBallBearingElement"

    @property
    def loaded_multi_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2227.LoadedMultiPointContactBallBearingElement":
        return self.__parent__._cast(_2227.LoadedMultiPointContactBallBearingElement)

    @property
    def loaded_ball_bearing_element(
        self: "CastSelf",
    ) -> "_2208.LoadedBallBearingElement":
        from mastapy._private.bearings.bearing_results.rolling import _2208

        return self.__parent__._cast(_2208.LoadedBallBearingElement)

    @property
    def loaded_element(self: "CastSelf") -> "_2222.LoadedElement":
        from mastapy._private.bearings.bearing_results.rolling import _2222

        return self.__parent__._cast(_2222.LoadedElement)

    @property
    def loaded_four_point_contact_ball_bearing_element(
        self: "CastSelf",
    ) -> "LoadedFourPointContactBallBearingElement":
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
class LoadedFourPointContactBallBearingElement(
    _2227.LoadedMultiPointContactBallBearingElement
):
    """LoadedFourPointContactBallBearingElement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_FOUR_POINT_CONTACT_BALL_BEARING_ELEMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def approximate_percentage_of_friction_used_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ApproximatePercentageOfFrictionUsedOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactAngleOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_outer_left(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchPressureVelocityOuterLeft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_pressure_velocity_outer_right(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchPressureVelocityOuterRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_outer_left(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactPatchSlidingSpeedOuterLeft")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_speed_outer_right(
        self: "Self",
    ) -> "_2038.PlaneScalarFieldData":
        """mastapy.utility.vectors.PlaneScalarFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingSpeedOuterRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_outer_left(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingVelocityOuterLeft"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def contact_patch_sliding_velocity_outer_right(
        self: "Self",
    ) -> "_2037.PlaneVectorFieldData":
        """mastapy.utility.vectors.PlaneVectorFieldData

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactPatchSlidingVelocityOuterRight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def curvature_moment_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def curvature_moment_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CurvatureMomentOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMajorDimensionOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_major_dimension_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMajorDimensionOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMinorDimensionOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_semi_minor_dimension_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianSemiMinorDimensionOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicPressureForceOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_pressure_force_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicPressureForceOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hydrodynamic_rolling_resistance_force_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HydrodynamicRollingResistanceForceOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_normal_stress_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumNormalStressOuterRight")

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
    def maximum_shear_stress_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_shear_stress_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumShearStressOuterRight")

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
    def minimum_lubricating_film_thickness_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_lubricating_film_thickness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumLubricatingFilmThicknessOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalLoadOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_load_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalLoadOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pivoting_moment_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PivotingMomentOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossOuterLeft")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerLossOuterRight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_outer_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_elastic_rolling_resistance_outer_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToElasticRollingResistanceOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_outer_left(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_due_to_hydrodynamic_rolling_resistance_outer_right(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossDueToHydrodynamicRollingResistanceOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMajorAxisOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_major_axis_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMajorAxisOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMinorAxisOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def power_loss_parallel_to_minor_axis_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerLossParallelToMinorAxisOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_major_axis_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMajorAxisOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_outer_left(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisOuterLeft"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_force_parallel_to_the_minor_axis_outer_right(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingForceParallelToTheMinorAxisOuterRight"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedFourPointContactBallBearingElement":
        """Cast to another type.

        Returns:
            _Cast_LoadedFourPointContactBallBearingElement
        """
        return _Cast_LoadedFourPointContactBallBearingElement(self)
