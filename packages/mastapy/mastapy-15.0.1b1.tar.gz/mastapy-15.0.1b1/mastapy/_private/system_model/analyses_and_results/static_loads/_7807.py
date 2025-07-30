"""PlanetManufactureError"""

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

_PLANET_MANUFACTURE_ERROR = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "PlanetManufactureError"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlanetManufactureError")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetManufactureError._Cast_PlanetManufactureError"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetManufactureError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetManufactureError:
    """Special nested class for casting PlanetManufactureError to subclasses."""

    __parent__: "PlanetManufactureError"

    @property
    def planet_manufacture_error(self: "CastSelf") -> "PlanetManufactureError":
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
class PlanetManufactureError(_0.APIBase):
    """PlanetManufactureError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_MANUFACTURE_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_of_error_in_pin_coordinate_system(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngleOfErrorInPinCoordinateSystem")

        if temp is None:
            return 0.0

        return temp

    @angle_of_error_in_pin_coordinate_system.setter
    @exception_bridge
    @enforce_parameter_types
    def angle_of_error_in_pin_coordinate_system(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AngleOfErrorInPinCoordinateSystem",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def angular_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AngularError")

        if temp is None:
            return 0.0

        return temp

    @angular_error.setter
    @exception_bridge
    @enforce_parameter_types
    def angular_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AngularError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def hole_radial_displacement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HoleRadialDisplacement")

        if temp is None:
            return 0.0

        return temp

    @hole_radial_displacement.setter
    @exception_bridge
    @enforce_parameter_types
    def hole_radial_displacement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "HoleRadialDisplacement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def radial_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialError")

        if temp is None:
            return 0.0

        return temp

    @radial_error.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radial_error_carrier(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialErrorCarrier")

        if temp is None:
            return 0.0

        return temp

    @radial_error_carrier.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_error_carrier(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RadialErrorCarrier",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def radial_tilt_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RadialTiltError")

        if temp is None:
            return 0.0

        return temp

    @radial_tilt_error.setter
    @exception_bridge
    @enforce_parameter_types
    def radial_tilt_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RadialTiltError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tangential_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TangentialError")

        if temp is None:
            return 0.0

        return temp

    @tangential_error.setter
    @exception_bridge
    @enforce_parameter_types
    def tangential_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TangentialError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tangential_tilt_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TangentialTiltError")

        if temp is None:
            return 0.0

        return temp

    @tangential_tilt_error.setter
    @exception_bridge
    @enforce_parameter_types
    def tangential_tilt_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TangentialTiltError",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def x_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XError")

        if temp is None:
            return 0.0

        return temp

    @x_error.setter
    @exception_bridge
    @enforce_parameter_types
    def x_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def x_tilt_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "XTiltError")

        if temp is None:
            return 0.0

        return temp

    @x_tilt_error.setter
    @exception_bridge
    @enforce_parameter_types
    def x_tilt_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "XTiltError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def y_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YError")

        if temp is None:
            return 0.0

        return temp

    @y_error.setter
    @exception_bridge
    @enforce_parameter_types
    def y_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YError", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def y_tilt_error(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "YTiltError")

        if temp is None:
            return 0.0

        return temp

    @y_tilt_error.setter
    @exception_bridge
    @enforce_parameter_types
    def y_tilt_error(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "YTiltError", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetManufactureError":
        """Cast to another type.

        Returns:
            _Cast_PlanetManufactureError
        """
        return _Cast_PlanetManufactureError(self)
