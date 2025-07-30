"""VirtualCylindricalGearSetISO10300MethodB2"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _482, _483

_VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "VirtualCylindricalGearSetISO10300MethodB2",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _471, _474

    Self = TypeVar("Self", bound="VirtualCylindricalGearSetISO10300MethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualCylindricalGearSetISO10300MethodB2._Cast_VirtualCylindricalGearSetISO10300MethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearSetISO10300MethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearSetISO10300MethodB2:
    """Special nested class for casting VirtualCylindricalGearSetISO10300MethodB2 to subclasses."""

    __parent__: "VirtualCylindricalGearSetISO10300MethodB2"

    @property
    def virtual_cylindrical_gear_set(
        self: "CastSelf",
    ) -> "_483.VirtualCylindricalGearSet":
        return self.__parent__._cast(_483.VirtualCylindricalGearSet)

    @property
    def bevel_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_471.BevelVirtualCylindricalGearSetISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _471

        return self.__parent__._cast(
            _471.BevelVirtualCylindricalGearSetISO10300MethodB2
        )

    @property
    def hypoid_virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_474.HypoidVirtualCylindricalGearSetISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _474

        return self.__parent__._cast(
            _474.HypoidVirtualCylindricalGearSetISO10300MethodB2
        )

    @property
    def virtual_cylindrical_gear_set_iso10300_method_b2(
        self: "CastSelf",
    ) -> "VirtualCylindricalGearSetISO10300MethodB2":
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
class VirtualCylindricalGearSetISO10300MethodB2(
    _483.VirtualCylindricalGearSet[_482.VirtualCylindricalGearISO10300MethodB2]
):
    """VirtualCylindricalGearSetISO10300MethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_SET_ISO10300_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_contact_direction_and_tooth_tangent_in_pitch_plane(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenContactDirectionAndToothTangentInPitchPlane"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_between_projection_of_pinion_axis_and_direction_of_contact_in_pitch_plane(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AngleBetweenProjectionOfPinionAxisAndDirectionOfContactInPitchPlane",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_between_projection_of_wheel_axis_and_direction_of_contact_in_pitch_plane(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AngleBetweenProjectionOfWheelAxisAndDirectionOfContactInPitchPlane",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angle_of_contact_line_relative_to_root_cone(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleOfContactLineRelativeToRootCone"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def angular_pitch_of_virtual_cylindrical_wheel(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularPitchOfVirtualCylindricalWheel"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_shift_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactShiftFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_base_spiral_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanBaseSpiralAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def modified_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ModifiedContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_base_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeBaseFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeFaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_in_normal_section(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeLengthOfActionInNormalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_normal_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMeanNormalBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearSetISO10300MethodB2":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearSetISO10300MethodB2
        """
        return _Cast_VirtualCylindricalGearSetISO10300MethodB2(self)
