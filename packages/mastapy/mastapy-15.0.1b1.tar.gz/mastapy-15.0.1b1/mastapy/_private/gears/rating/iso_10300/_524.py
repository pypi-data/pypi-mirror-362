"""ISO10300SingleFlankRatingMethodB2"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _482

_ISO10300_SINGLE_FLANK_RATING_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300SingleFlankRatingMethodB2"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _455
    from mastapy._private.gears.rating.conical import _634
    from mastapy._private.gears.rating.iso_10300 import _521, _522

    Self = TypeVar("Self", bound="ISO10300SingleFlankRatingMethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300SingleFlankRatingMethodB2._Cast_ISO10300SingleFlankRatingMethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300SingleFlankRatingMethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300SingleFlankRatingMethodB2:
    """Special nested class for casting ISO10300SingleFlankRatingMethodB2 to subclasses."""

    __parent__: "ISO10300SingleFlankRatingMethodB2"

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
    def iso10300_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "ISO10300SingleFlankRatingMethodB2":
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
class ISO10300SingleFlankRatingMethodB2(
    _520.ISO10300SingleFlankRating[_482.VirtualCylindricalGearISO10300MethodB2]
):
    """ISO10300SingleFlankRatingMethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_SINGLE_FLANK_RATING_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def combined_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_stress_adjustment_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressAdjustmentFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cos_pressure_angle_at_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CosPressureAngleAtPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heel_increment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeelIncrement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def heel_increment_delta_be(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HeelIncrementDeltaBe")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inertia_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def L(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "L")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def m(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "M")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_value_of_root_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NominalValueOfRootStressMethodB2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "O")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_contact_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleContactStressMethodB2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_tooth_root_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleToothRootStressMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pressure_angle_at_point_of_load_application(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PressureAngleAtPointOfLoadApplication"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def projected_length_of_the_instantaneous_contact_line_in_the_tooth_lengthwise_direction(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "ProjectedLengthOfTheInstantaneousContactLineInTheToothLengthwiseDirection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_of_curvature_difference_between_point_of_load_and_mean_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusOfCurvatureDifferenceBetweenPointOfLoadAndMeanPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_fillet_radius_at_root_of_tooth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeFilletRadiusAtRootOfTooth")

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
    def relative_surface_condition_factor_for_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeSurfaceConditionFactorForMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_stress_adjustment_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootStressAdjustmentFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_bending_for_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorBendingForMethodB2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def safety_factor_contact_for_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorContactForMethodB2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_concentration_and_correction_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressConcentrationAndCorrectionFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def toe_increment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToeIncrement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def toe_increment_delta_bi(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToeIncrementDeltaBi")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootStressMethodB2")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300SingleFlankRatingMethodB2":
        """Cast to another type.

        Returns:
            _Cast_ISO10300SingleFlankRatingMethodB2
        """
        return _Cast_ISO10300SingleFlankRatingMethodB2(self)
