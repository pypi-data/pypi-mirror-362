"""VehicleDynamicsProperties"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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

_VEHICLE_DYNAMICS_PROPERTIES = python_net_import(
    "SMT.MastaAPI.Materials", "VehicleDynamicsProperties"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VehicleDynamicsProperties")
    CastSelf = TypeVar(
        "CastSelf", bound="VehicleDynamicsProperties._Cast_VehicleDynamicsProperties"
    )


__docformat__ = "restructuredtext en"
__all__ = ("VehicleDynamicsProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_VehicleDynamicsProperties:
    """Special nested class for casting VehicleDynamicsProperties to subclasses."""

    __parent__: "VehicleDynamicsProperties"

    @property
    def vehicle_dynamics_properties(self: "CastSelf") -> "VehicleDynamicsProperties":
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
class VehicleDynamicsProperties(_0.APIBase):
    """VehicleDynamicsProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _VEHICLE_DYNAMICS_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def aerodynamic_drag_coefficient(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AerodynamicDragCoefficient")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def air_density(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AirDensity")

        if temp is None:
            return 0.0

        return temp

    @air_density.setter
    @exception_bridge
    @enforce_parameter_types
    def air_density(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AirDensity", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def drag_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DragCoefficient")

        if temp is None:
            return 0.0

        return temp

    @drag_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def drag_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "DragCoefficient", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_wheels(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfWheels")

        if temp is None:
            return 0

        return temp

    @number_of_wheels.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_wheels(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfWheels", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def rolling_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingRadius")

        if temp is None:
            return 0.0

        return temp

    @rolling_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollingRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rolling_resistance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollingResistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rolling_resistance_coefficient(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingResistanceCoefficient")

        if temp is None:
            return 0.0

        return temp

    @rolling_resistance_coefficient.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_resistance_coefficient(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RollingResistanceCoefficient",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vehicle_effective_inertia(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleEffectiveInertia")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_effective_mass(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleEffectiveMass")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def vehicle_frontal_area(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleFrontalArea")

        if temp is None:
            return 0.0

        return temp

    @vehicle_frontal_area.setter
    @exception_bridge
    @enforce_parameter_types
    def vehicle_frontal_area(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "VehicleFrontalArea",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def vehicle_mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "VehicleMass")

        if temp is None:
            return 0.0

        return temp

    @vehicle_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def vehicle_mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "VehicleMass", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wheel_inertia(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "WheelInertia")

        if temp is None:
            return 0.0

        return temp

    @wheel_inertia.setter
    @exception_bridge
    @enforce_parameter_types
    def wheel_inertia(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "WheelInertia", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_VehicleDynamicsProperties":
        """Cast to another type.

        Returns:
            _Cast_VehicleDynamicsProperties
        """
        return _Cast_VehicleDynamicsProperties(self)
