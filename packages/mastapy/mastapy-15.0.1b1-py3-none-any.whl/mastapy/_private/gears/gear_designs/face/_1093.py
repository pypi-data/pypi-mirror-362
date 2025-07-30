"""FaceGearDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1051

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_FACE_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face", "FaceGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears import _423
    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.face import _1098, _1101

    Self = TypeVar("Self", bound="FaceGearDesign")
    CastSelf = TypeVar("CastSelf", bound="FaceGearDesign._Cast_FaceGearDesign")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearDesign:
    """Special nested class for casting FaceGearDesign to subclasses."""

    __parent__: "FaceGearDesign"

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def face_gear_pinion_design(self: "CastSelf") -> "_1098.FaceGearPinionDesign":
        from mastapy._private.gears.gear_designs.face import _1098

        return self.__parent__._cast(_1098.FaceGearPinionDesign)

    @property
    def face_gear_wheel_design(self: "CastSelf") -> "_1101.FaceGearWheelDesign":
        from mastapy._private.gears.gear_designs.face import _1101

        return self.__parent__._cast(_1101.FaceGearWheelDesign)

    @property
    def face_gear_design(self: "CastSelf") -> "FaceGearDesign":
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
class FaceGearDesign(_1051.GearDesign):
    """FaceGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def hand(self: "Self") -> "_423.Hand":
        """mastapy.gears.Hand"""
        temp = pythonnet_property_get(self.wrapped, "Hand")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.Hand")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._423", "Hand")(
            value
        )

    @hand.setter
    @exception_bridge
    @enforce_parameter_types
    def hand(self: "Self", value: "_423.Hand") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.Hand")
        pythonnet_property_set(self.wrapped, "Hand", value)

    @property
    @exception_bridge
    def iso_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ISOMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @iso_material.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ISOMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def mean_point_to_crossing_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanPointToCrossingPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pitch_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PitchAngle")

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
    @exception_bridge
    def working_pitch_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPitchRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearDesign":
        """Cast to another type.

        Returns:
            _Cast_FaceGearDesign
        """
        return _Cast_FaceGearDesign(self)
