"""WormGearSetDesign"""

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

_WORM_GEAR_SET_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Worm", "WormGearSetDesign"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _441
    from mastapy._private.gears.gear_designs import _1052
    from mastapy._private.gears.gear_designs.worm import _1061, _1062

    Self = TypeVar("Self", bound="WormGearSetDesign")
    CastSelf = TypeVar("CastSelf", bound="WormGearSetDesign._Cast_WormGearSetDesign")


__docformat__ = "restructuredtext en"
__all__ = ("WormGearSetDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_WormGearSetDesign:
    """Special nested class for casting WormGearSetDesign to subclasses."""

    __parent__: "WormGearSetDesign"

    @property
    def gear_set_design(self: "CastSelf") -> "_1054.GearSetDesign":
        return self.__parent__._cast(_1054.GearSetDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def worm_gear_set_design(self: "CastSelf") -> "WormGearSetDesign":
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
class WormGearSetDesign(_1054.GearSetDesign):
    """WormGearSetDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _WORM_GEAR_SET_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def axial_module(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialModule")

        if temp is None:
            return 0.0

        return temp

    @axial_module.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_module(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AxialModule", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def axial_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @axial_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def normal_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @normal_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def worm_type(self: "Self") -> "_441.WormType":
        """mastapy.gears.WormType"""
        temp = pythonnet_property_get(self.wrapped, "WormType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.WormType")

        if value is None:
            return None

        return constructor.new_from_mastapy("mastapy._private.gears._441", "WormType")(
            value
        )

    @worm_type.setter
    @exception_bridge
    @enforce_parameter_types
    def worm_type(self: "Self", value: "_441.WormType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Gears.WormType")
        pythonnet_property_set(self.wrapped, "WormType", value)

    @property
    @exception_bridge
    def gears(self: "Self") -> "List[_1061.WormGearDesign]":
        """List[mastapy.gears.gear_designs.worm.WormGearDesign]

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
    def worm_gears(self: "Self") -> "List[_1061.WormGearDesign]":
        """List[mastapy.gears.gear_designs.worm.WormGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def worm_meshes(self: "Self") -> "List[_1062.WormGearMeshDesign]":
        """List[mastapy.gears.gear_designs.worm.WormGearMeshDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WormMeshes")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_WormGearSetDesign":
        """Cast to another type.

        Returns:
            _Cast_WormGearSetDesign
        """
        return _Cast_WormGearSetDesign(self)
