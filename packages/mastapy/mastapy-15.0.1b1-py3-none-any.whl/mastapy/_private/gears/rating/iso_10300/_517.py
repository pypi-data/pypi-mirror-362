"""ISO10300MeshSingleFlankRatingMethodB2"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _482

_ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "ISO10300MeshSingleFlankRatingMethodB2"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating import _457
    from mastapy._private.gears.rating.conical import _637
    from mastapy._private.gears.rating.iso_10300 import _514, _515
    from mastapy._private.gears.rating.virtual_cylindrical_gears import _485

    Self = TypeVar("Self", bound="ISO10300MeshSingleFlankRatingMethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO10300MeshSingleFlankRatingMethodB2._Cast_ISO10300MeshSingleFlankRatingMethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO10300MeshSingleFlankRatingMethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO10300MeshSingleFlankRatingMethodB2:
    """Special nested class for casting ISO10300MeshSingleFlankRatingMethodB2 to subclasses."""

    __parent__: "ISO10300MeshSingleFlankRatingMethodB2"

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
    def iso10300_mesh_single_flank_rating_bevel_method_b2(
        self: "CastSelf",
    ) -> "_514.ISO10300MeshSingleFlankRatingBevelMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _514

        return self.__parent__._cast(_514.ISO10300MeshSingleFlankRatingBevelMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_hypoid_method_b2(
        self: "CastSelf",
    ) -> "_515.ISO10300MeshSingleFlankRatingHypoidMethodB2":
        from mastapy._private.gears.rating.iso_10300 import _515

        return self.__parent__._cast(_515.ISO10300MeshSingleFlankRatingHypoidMethodB2)

    @property
    def iso10300_mesh_single_flank_rating_method_b2(
        self: "CastSelf",
    ) -> "ISO10300MeshSingleFlankRatingMethodB2":
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
class ISO10300MeshSingleFlankRatingMethodB2(
    _513.ISO10300MeshSingleFlankRating[_482.VirtualCylindricalGearISO10300MethodB2]
):
    """ISO10300MeshSingleFlankRatingMethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO10300_MESH_SINGLE_FLANK_RATING_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def contact_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactStressMethodB2")

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
    def face_width_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inertia_factor_value_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InertiaFactorValueX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def intermediate_value_x(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IntermediateValueX")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_action_at_critical_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfActionAtCriticalPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_action_considering_adjacent_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfActionConsideringAdjacentTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LengthOfContactLine")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_ratio_for_bending_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadSharingRatioForBendingMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_sharing_ratio_for_pitting_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadSharingRatioForPittingMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def nominal_value_of_contact_stress_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NominalValueOfContactStressMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pinion_profile_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionProfileRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitting_resistance_geometry_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PittingResistanceGeometryFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def position_change_alone_path_of_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PositionChangeAlonePathOfContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_of_curvature_change(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusOfCurvatureChange")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_ellipse_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeLengthOfActionEllipseContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_ellipse_contact_for_statically_loaded_straight_bevel_and_zerol_bevel_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "RelativeLengthOfActionEllipseContactForStaticallyLoadedStraightBevelAndZerolBevelGears",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_within_the_contact_ellipse(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeLengthOfActionWithinTheContactEllipse"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_radius_of_profile_curvature_between_pinion_and_wheel(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeRadiusOfProfileCurvatureBetweenPinionAndWheel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factors_for_bending_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorsForBendingMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_load_factors_for_contact_method_b2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransverseLoadFactorsForContactMethodB2"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_profile_radius_of_curvature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelProfileRadiusOfCurvature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yi(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YI")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yi_for_bevel_and_zerol_bevel_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YIForBevelAndZerolBevelGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yi_for_hypoid_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "YIForHypoidGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_cylindrical_gear_set_method_b2(
        self: "Self",
    ) -> "_485.VirtualCylindricalGearSetISO10300MethodB2":
        """mastapy.gears.rating.virtual_cylindrical_gears.VirtualCylindricalGearSetISO10300MethodB2

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualCylindricalGearSetMethodB2")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_ISO10300MeshSingleFlankRatingMethodB2":
        """Cast to another type.

        Returns:
            _Cast_ISO10300MeshSingleFlankRatingMethodB2
        """
        return _Cast_ISO10300MeshSingleFlankRatingMethodB2(self)
