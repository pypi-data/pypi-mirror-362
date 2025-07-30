"""HypoidVirtualCylindricalGearSetISO10300MethodB2"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _485

_HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "HypoidVirtualCylindricalGearSetISO10300MethodB2",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

    Self = TypeVar("Self", bound="HypoidVirtualCylindricalGearSetISO10300MethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HypoidVirtualCylindricalGearSetISO10300MethodB2._Cast_HypoidVirtualCylindricalGearSetISO10300MethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HypoidVirtualCylindricalGearSetISO10300MethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB2:
    """Special nested class for casting HypoidVirtualCylindricalGearSetISO10300MethodB2 to subclasses."""

    __parent__: "HypoidVirtualCylindricalGearSetISO10300MethodB2"

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_485.VirtualCylindricalGearSetISO10300MethodB2":
        return self.__parent__._cast(_485.VirtualCylindricalGearSetISO10300MethodB2)

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        pass

        from mastapy._private.gears.rating.virtual_cylindrical_gears import _483

        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "HypoidVirtualCylindricalGearSetISO10300MethodB2":
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
class HypoidVirtualCylindricalGearSetISO10300MethodB2(
    _485.VirtualCylindricalGearSetISO10300MethodB2
):
    """HypoidVirtualCylindricalGearSetISO10300MethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _HYPOID_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_direction_of_contact_and_the_pitch_tangent(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenDirectionOfContactAndThePitchTangent"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_pressure_angle_unbalance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AveragePressureAngleUnbalance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def coast_flank_pressure_angel_in_wheel_root_coordinates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CoastFlankPressureAngelInWheelRootCoordinates"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def drive_flank_pressure_angel_in_wheel_root_coordinates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DriveFlankPressureAngelInWheelRootCoordinates"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def initial_value_for_the_wheel_angle_from_centreline_to_fillet_point_on_drive_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "InitialValueForTheWheelAngleFromCentrelineToFilletPointOnDriveFlank",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_action_from_pinion_tip_to_pitch_circle_in_normal_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfActionFromPinionTipToPitchCircleInNormalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def length_of_action_from_wheel_tip_to_pitch_circle_in_normal_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LengthOfActionFromWheelTipToPitchCircleInNormalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limit_pressure_angle_in_wheel_root_coordinates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LimitPressureAngleInWheelRootCoordinates"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_contact_ratio_for_hypoid_gears(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ModifiedContactRatioForHypoidGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_distance_from_blade_edge_to_centreline(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeDistanceFromBladeEdgeToCentreline"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_centreline_to_fillet_point_on_drive_flank(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleFromCentrelineToFilletPointOnDriveFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_centreline_to_pinion_tip_on_drive_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WheelAngleFromCentrelineToPinionTipOnDriveSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_angle_from_centreline_to_tooth_surface_at_pitch_point_on_drive_side(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "WheelAngleFromCentrelineToToothSurfaceAtPitchPointOnDriveSide",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def wheel_mean_slot_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WheelMeanSlotWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h1o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H1o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H2")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def h2o(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "H2o")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar_1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def deltar_2(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Deltar2")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(
        self: "Self",
    ) -> "_Cast_HypoidVirtualCylindricalGearSetISO10300MethodB2":
        """Cast to another type.

        Returns:
            _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB2
        """
        return _Cast_HypoidVirtualCylindricalGearSetISO10300MethodB2(self)
