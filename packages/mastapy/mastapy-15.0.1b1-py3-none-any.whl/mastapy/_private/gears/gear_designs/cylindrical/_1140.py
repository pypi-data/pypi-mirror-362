"""CylindricalGearSetMacroGeometryOptimiser"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears import _421

_CYLINDRICAL_GEAR_SET_MACRO_GEOMETRY_OPTIMISER = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical",
    "CylindricalGearSetMacroGeometryOptimiser",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearSetMacroGeometryOptimiser")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearSetMacroGeometryOptimiser._Cast_CylindricalGearSetMacroGeometryOptimiser",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearSetMacroGeometryOptimiser",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearSetMacroGeometryOptimiser:
    """Special nested class for casting CylindricalGearSetMacroGeometryOptimiser to subclasses."""

    __parent__: "CylindricalGearSetMacroGeometryOptimiser"

    @property
    def gear_set_optimiser(self: "CastSelf") -> "_421.GearSetOptimiser":
        return self.__parent__._cast(_421.GearSetOptimiser)

    @property
    def cylindrical_gear_set_macro_geometry_optimiser(
        self: "CastSelf",
    ) -> "CylindricalGearSetMacroGeometryOptimiser":
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
class CylindricalGearSetMacroGeometryOptimiser(_421.GearSetOptimiser):
    """CylindricalGearSetMacroGeometryOptimiser

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SET_MACRO_GEOMETRY_OPTIMISER

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def modify_basic_rack(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ModifyBasicRack")

        if temp is None:
            return False

        return temp

    @modify_basic_rack.setter
    @exception_bridge
    @enforce_parameter_types
    def modify_basic_rack(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "ModifyBasicRack", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def modify_planet_carrier_diameter(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ModifyPlanetCarrierDiameter")

        if temp is None:
            return False

        return temp

    @modify_planet_carrier_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def modify_planet_carrier_diameter(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModifyPlanetCarrierDiameter",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def planet_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PlanetDiameter")

        if temp is None:
            return 0.0

        return temp

    @planet_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def planet_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "PlanetDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def use_compressed_duty_cycle(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseCompressedDutyCycle")

        if temp is None:
            return False

        return temp

    @use_compressed_duty_cycle.setter
    @exception_bridge
    @enforce_parameter_types
    def use_compressed_duty_cycle(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseCompressedDutyCycle",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def helix_angle_input_is_active(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngleInputIsActive")

        if temp is None:
            return False

        return temp

    @helix_angle_input_is_active.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle_input_is_active(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HelixAngleInputIsActive",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def pressure_angle_input_is_active(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "PressureAngleInputIsActive")

        if temp is None:
            return False

        return temp

    @pressure_angle_input_is_active.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure_angle_input_is_active(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PressureAngleInputIsActive",
            bool(value) if value is not None else False,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearSetMacroGeometryOptimiser":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearSetMacroGeometryOptimiser
        """
        return _Cast_CylindricalGearSetMacroGeometryOptimiser(self)
