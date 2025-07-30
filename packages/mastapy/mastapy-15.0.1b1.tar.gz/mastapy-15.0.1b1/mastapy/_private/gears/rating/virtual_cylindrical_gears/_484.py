"""VirtualCylindricalGearSetISO10300MethodB1"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _481, _483

_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "VirtualCylindricalGearSetISO10300MethodB1",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _470, _473

    Self = TypeVar("Self", bound="VirtualCylindricalGearSetISO10300MethodB1")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualCylindricalGearSetISO10300MethodB1._Cast_VirtualCylindricalGearSetISO10300MethodB1",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearSetISO10300MethodB1",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearSetISO10300MethodB1:
    """Special nested class for casting VirtualCylindricalGearSetISO10300MethodB1 to subclasses."""

    __parent__: "VirtualCylindricalGearSetISO10300MethodB1"

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def bevel_virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_470.BevelVirtualCylindricalGearSetISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _470

        return self.__parent__._cast(
            _470.BevelVirtualCylindricalGearSetISO10300MethodB1
        )

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "_473.HypoidVirtualCylindricalGearSetISO10300MethodB1":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _473

        return self.__parent__._cast(
            _473.HypoidVirtualCylindricalGearSetISO10300MethodB1
        )

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b1(
        self: "CastSelf",
    ) -> "VirtualCylindricalGearSetISO10300MethodB1":
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
class VirtualCylindricalGearSetISO10300MethodB1(
    _483.VirtualCylindricalGearSet[_481.VirtualCylindricalGearISO10300MethodB1]
):
    """VirtualCylindricalGearSetISO10300MethodB1

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B1

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auxiliary_angle_for_virtual_face_width_method_b1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AuxiliaryAngleForVirtualFaceWidthMethodB1"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def correction_factor_for_theoretical_length_of_middle_contact_line_for_surface_durability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "CorrectionFactorForTheoreticalLengthOfMiddleContactLineForSurfaceDurability",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_middle_contact_line_in_the_zone_of_action_for_surface_durability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheMiddleContactLineInTheZoneOfActionForSurfaceDurability",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_middle_contact_line_in_the_zone_of_action_for_tooth_root_strength(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheMiddleContactLineInTheZoneOfActionForToothRootStrength",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_root_contact_line_in_the_zone_of_action_for_surface_durability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheRootContactLineInTheZoneOfActionForSurfaceDurability",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_root_contact_line_in_the_zone_of_action_for_tooth_root_strength(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheRootContactLineInTheZoneOfActionForToothRootStrength",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_tip_contact_line_in_the_zone_of_action_for_surface_durability(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheTipContactLineInTheZoneOfActionForSurfaceDurability",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_tip_contact_line_in_the_zone_of_action_for_tooth_root_strength(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DistanceOfTheTipContactLineInTheZoneOfActionForToothRootStrength",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inclination_angle_of_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InclinationAngleOfContactLine")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_middle_contact_line_for_surface_durability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfMiddleContactLineForSurfaceDurability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_middle_contact_line_for_tooth_root_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfMiddleContactLineForToothRootStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_path_of_contact_of_virtual_cylindrical_gear_in_transverse_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "LengthOfPathOfContactOfVirtualCylindricalGearInTransverseSection",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_root_contact_line_for_surface_durability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfRootContactLineForSurfaceDurability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_root_contact_line_for_tooth_root_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfRootContactLineForToothRootStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_tip_contact_line_for_surface_durability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfTipContactLineForSurfaceDurability"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_tip_contact_line_for_tooth_root_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfTipContactLineForToothRootStrength"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_distance_from_middle_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumDistanceFromMiddleContactLine"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_distance_from_middle_contact_line_at_left_side_of_contact_pattern(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MaximumDistanceFromMiddleContactLineAtLeftSideOfContactPattern",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_distance_from_middle_contact_line_at_right_side_of_contact_pattern(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "MaximumDistanceFromMiddleContactLineAtRightSideOfContactPattern",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def projected_auxiliary_angle_for_length_of_contact_line(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProjectedAuxiliaryAngleForLengthOfContactLine"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_of_relative_curvature_in_normal_section_at_the_mean_point(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusOfRelativeCurvatureInNormalSectionAtTheMeanPoint"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_of_relative_curvature_vertical_to_the_contact_line(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RadiusOfRelativeCurvatureVerticalToTheContactLine"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tan_auxiliary_angle_for_length_of_contact_line_calculation(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TanAuxiliaryAngleForLengthOfContactLineCalculation"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_effective_face_width_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelEffectiveFaceWidthFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearSetISO10300MethodB1":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearSetISO10300MethodB1
        """
        return _Cast_VirtualCylindricalGearSetISO10300MethodB1(self)
