"""FaceGearSetDesign"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.gear_designs import _1054

_FACE_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Face", "FaceGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.face import (
        _1093,
        _1095,
        _1098,
        _1100,
        _1101,
    )

    Self = TypeVar("Self", bound="FaceGearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="FaceGearSetDesign._Cast_FaceGearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("FaceGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_FaceGearSetDesign:
    """Special nested class for casting FaceGearSetDesign to subclasses."""

    __parent__: "FaceGearSetDesign"

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def face_gear_set_design(self: "CastSelf") -> "FaceGearSetDesign":
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
class FaceGearSetDesign(_1054.GearSetDesign):
    """FaceGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _FACE_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Module")

        if temp is None:
            return 0.0

        return temp

    @module.setter
    @exception_bridge
    @enforce_parameter_types
    def module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Module", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def nominal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NominalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @nominal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def nominal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NominalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_base_pitch(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalBasePitch")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftAngle")

        if temp is None:
            return 0.0

        return temp

    @shaft_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def working_normal_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingNormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cylindrical_gear_set_micro_geometry(
        self: "Self",
    ) -> "_1100.FaceGearSetMicroGeometry":
        """mastapy.gears.gear_designs.face.FaceGearSetMicroGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearSetMicroGeometry")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def face_gear(self: "Self") -> "_1101.FaceGearWheelDesign":
        """mastapy.gears.gear_designs.face.FaceGearWheelDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGear")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def pinion(self: "Self") -> "_1098.FaceGearPinionDesign":
        """mastapy.gears.gear_designs.face.FaceGearPinionDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Pinion")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1093.FaceGearDesign]":
        """List[mastapy.gears.gear_designs.face.FaceGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Gears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_gears(self: "Self") -> "List[_1093.FaceGearDesign]":
        """List[mastapy.gears.gear_designs.face.FaceGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_meshes(self: "Self") -> "List[_1095.FaceGearMeshDesign]":
        """List[mastapy.gears.gear_designs.face.FaceGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_FaceGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_FaceGearSetDesign
        """
        return _Cast_FaceGearSetDesign(self)
