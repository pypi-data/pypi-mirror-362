"""WormWheelDesign"""

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
from mastapy._private.gears.gear_designs.worm import _1061

_WORM_WHEEL_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Worm", "WormWheelDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051, _1052

    Self = TypeVar("Self", bound="WormWheelDesign")
    CastSelf = TypeVar("CastSelf", bound="WormWheelDesign._Cast_WormWheelDesign")


__docformat__ = "restructuredtext en"
__all__ = ("WormWheelDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormWheelDesign:
    """Special nested class for casting WormWheelDesign to subclasses."""

    __parent__: "WormWheelDesign"

    @property
    def worm_gear_design(self: "CastSelf") -> "_1061.WormGearDesign":
        return self.__parent__._cast(_1061.WormGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def worm_wheel_design(self: "CastSelf") -> "WormWheelDesign":
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
class WormWheelDesign(_1061.WormGearDesign):
    """WormWheelDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_WHEEL_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def face_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_helix_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanHelixAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reference_helix_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceHelixAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def root_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def throat_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThroatRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def throat_tip_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ThroatTipDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def working_pitch_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPitchDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_WormWheelDesign":
        """Cast to another type.

        Returns:
            _Cast_WormWheelDesign
        """
        return _Cast_WormWheelDesign(self)
