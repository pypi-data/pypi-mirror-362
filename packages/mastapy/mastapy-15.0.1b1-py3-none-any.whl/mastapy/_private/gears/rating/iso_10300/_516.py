"""ISO10300MeshSingleFlankRatingMethodB1"""

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
from mastapy._private.gears.rating.iso_10300 import _513
from mastapy._private.gears.rating.virtual_cylindrical_gears import _481

_ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B1 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300MeshSingleFlankRatingMethodB1"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.conical import _637
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _484

    Self = TypeVar("Self", bound="ISO10300MeshSingleFlankRatingMethodB1")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300MeshSingleFlankRatingMethodB1._Cast_ISO10300MeshSingleFlankRatingMethodB1",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300MeshSingleFlankRatingMethodB1",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300MeshSingleFlankRatingMethodB1:
    """Special nested class for casting ISO10300MeshSingleFlankRatingMethodB1 to subclasses."""

    __parent__: "ISO10300MeshSingleFlankRatingMethodB1"

    @property
    def iso10300_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_513.ISO10300MeshSingleFlankRating":
        return self.__parent__._cast(_513.ISO10300MeshSingleFlankRating)

    @property
    def conical_mesh_single_flank_rating(
        self: "CastSelf",
    ) -> "_637.ConicalMeshSingleFlankRating":
        from mastapy._private.gears.rating.conical import _637

        return self.__parent__._cast(_637.ConicalMeshSingleFlankRating)

    @property
    def mesh_single_flank_rating(self: "CastSelf") -> "_457.MeshSingleFlankRating":
        from mastapy._private.gears.rating import _457

        return self.__parent__._cast(_457.MeshSingleFlankRating)

    @property
    def iso10300_mesh_single_flank_rating_method_b1(
        self: "CastSelf",
    ) -> "ISO10300MeshSingleFlankRatingMethodB1":
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
class ISO10300MeshSingleFlankRatingMethodB1(
    _513.ISO10300MeshSingleFlankRating[_481.VirtualCylindricalGearISO10300MethodB1]
):
    """ISO10300MeshSingleFlankRatingMethodB1

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B1

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def area_above_the_middle_contact_line_for_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheMiddleContactLineForBending"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def area_above_the_middle_contact_line_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheMiddleContactLineForContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def area_above_the_root_contact_line_for_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheRootContactLineForBending"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def area_above_the_root_contact_line_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheRootContactLineForContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def area_above_the_tip_contact_line_for_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheTipContactLineForBending"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def area_above_the_tip_contact_line_for_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AreaAboveTheTipContactLineForContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_value_abs(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryValueABS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_value_bbs(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryValueBBS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def auxiliary_value_cbs(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryValueCBS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_tooth_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageToothDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bevel_gear_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelGearFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bevel_spiral_angle_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BevelSpiralAngleFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_ratio_factor_for_bending_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRatioFactorForBendingMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressMethodB1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress_use_bevel_slip_factor_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactStressUseBevelSlipFactorMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def developed_length_of_one_tooth_as_the_face_width_of_the_calculation_model(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DevelopedLengthOfOneToothAsTheFaceWidthOfTheCalculationModel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hypoid_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HypoidFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inclination_angle_of_the_sum_of_velocities_vector(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InclinationAngleOfTheSumOfVelocitiesVector"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_factor_pitting(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadSharingFactorPitting")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mid_zone_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MidZoneFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_normal_force_of_virtual_cylindrical_gear_at_mean_point_p(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalNormalForceOfVirtualCylindricalGearAtMeanPointP"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_value_of_contact_stress_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalValueOfContactStressMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_value_of_contact_stress_using_bevel_slip_factor_method_b1(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalValueOfContactStressUsingBevelSlipFactorMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def part_of_the_models_face_width_covered_by_the_constance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PartOfTheModelsFaceWidthCoveredByTheConstance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_bevel_slip_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionBevelSlipFactor")

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
    def sliding_velocity_at_mean_point_p(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocityAtMeanPointP")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity_parallel_to_the_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlidingVelocityParallelToTheContactLine"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_velocities(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumOfVelocities")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_velocities_in_lengthwise_direction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfVelocitiesInLengthwiseDirection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_velocities_in_profile_direction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SumOfVelocitiesInProfileDirection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sum_of_velocities_vertical_to_the_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SumOfVelocitiesVerticalToTheContactLine"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def the_ratio_of_maximum_load_over_the_middle_contact_line_and_total_load(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TheRatioOfMaximumLoadOverTheMiddleContactLineAndTotalLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factors_for_bending_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorsForBendingMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factors_for_contact_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorsForContactMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_bevel_slip_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelBevelSlipFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_cylindrical_gear_set_method_b1(
        self: "Self",
    ) -> "_484.VirtualCylindricalGearSetISO10300MethodB1":
        """mastapy.gears.rating.virtual_cylindrical_gears.VirtualCylindricalGearSetISO10300MethodB1

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualCylindricalGearSetMethodB1")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300MeshSingleFlankRatingMethodB1":
        """Cast to another type.

        Returns:
            _Cast_ISO10300MeshSingleFlankRatingMethodB1
        """
        return _Cast_ISO10300MeshSingleFlankRatingMethodB1(self)
