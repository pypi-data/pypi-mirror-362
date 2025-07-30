"""VirtualCylindricalGearISO10300MethodB2"""

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
from mastapy._private.gears.rating.virtual_cylindrical_gears import _480

_VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B2 = python_net_import(
    "SMT.MastaAPI.Gears.Rating.VirtualCylindricalGears",
    "VirtualCylindricalGearISO10300MethodB2",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.rating.virtual_cylindrical_gears import _469, _472

    Self = TypeVar("Self", bound="VirtualCylindricalGearISO10300MethodB2")
    CastSelf = TypeVar(
        "CastSelf",
        bound="VirtualCylindricalGearISO10300MethodB2._Cast_VirtualCylindricalGearISO10300MethodB2",
    )


__docformat__ = "restructuredtext en"
__all__ = ("VirtualCylindricalGearISO10300MethodB2",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VirtualCylindricalGearISO10300MethodB2:
    """Special nested class for casting VirtualCylindricalGearISO10300MethodB2 to subclasses."""

    __parent__: "VirtualCylindricalGearISO10300MethodB2"

    @property
    def virtual_cylindrical_gear_basic(
        self: "CastSelf",
    ) -> "_480.VirtualCylindricalGearBasic":
        return self.__parent__._cast(_480.VirtualCylindricalGearBasic)

    @property
    def bevel_virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_469.BevelVirtualCylindricalGearISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _469

        return self.__parent__._cast(_469.BevelVirtualCylindricalGearISO10300MethodB2)

    @property
    def hypoid_virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "_472.HypoidVirtualCylindricalGearISO10300MethodB2":
        from mastapy._private.gears.rating.virtual_cylindrical_gears import _472

        return self.__parent__._cast(_472.HypoidVirtualCylindricalGearISO10300MethodB2)

    @property
    def virtual_cylindrical_gear_iso10300_method_b2(
        self: "CastSelf",
    ) -> "VirtualCylindricalGearISO10300MethodB2":
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
class VirtualCylindricalGearISO10300MethodB2(_480.VirtualCylindricalGearBasic):
    """VirtualCylindricalGearISO10300MethodB2

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VIRTUAL_CYLINDRICAL_GEAR_ISO10300_METHOD_B2

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjusted_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_edge_radius_of_tool(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeEdgeRadiusOfTool")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_length_of_action_from_tip_to_pitch_circle_in_normal_section(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeLengthOfActionFromTipToPitchCircleInNormalSection"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_back_cone_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMeanBackConeDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_base_radius_of_virtual_cylindrical_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeMeanBaseRadiusOfVirtualCylindricalGear"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_normal_pitch_for_virtual_cylindrical_gears(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "RelativeMeanNormalPitchForVirtualCylindricalGears"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_virtual_dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMeanVirtualDedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_virtual_pitch_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMeanVirtualPitchRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_mean_virtual_tip_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeMeanVirtualTipRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_virtual_tooth_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeVirtualToothThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_VirtualCylindricalGearISO10300MethodB2":
        """Cast to another type.

        Returns:
            _Cast_VirtualCylindricalGearISO10300MethodB2
        """
        return _Cast_VirtualCylindricalGearISO10300MethodB2(self)
