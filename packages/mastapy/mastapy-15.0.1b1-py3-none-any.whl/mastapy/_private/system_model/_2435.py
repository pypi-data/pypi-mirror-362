"""TransmissionTemperatureSet"""

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

_TRANSMISSION_TEMPERATURE_SET = python_net_import(
    "SMT.MastaAPI.SystemModel", "TransmissionTemperatureSet"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TransmissionTemperatureSet")
    CastSelf = TypeVar(
        "CastSelf", bound="TransmissionTemperatureSet._Cast_TransmissionTemperatureSet"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransmissionTemperatureSet",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_TransmissionTemperatureSet:
    """Special nested class for casting TransmissionTemperatureSet to subclasses."""

    __parent__: "TransmissionTemperatureSet"

    @property
    def transmission_temperature_set(self: "CastSelf") -> "TransmissionTemperatureSet":
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
class TransmissionTemperatureSet(_0.APIBase):
    """TransmissionTemperatureSet

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TRANSMISSION_TEMPERATURE_SET

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def air_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AirTemperature")

        if temp is None:
            return 0.0

        return temp

    @air_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def air_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AirTemperature", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def housing(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Housing")

        if temp is None:
            return 0.0

        return temp

    @housing.setter
    @exception_bridge
    @enforce_parameter_types
    def housing(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Housing", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def oil_sump_and_inlet_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OilSumpAndInletTemperature")

        if temp is None:
            return 0.0

        return temp

    @oil_sump_and_inlet_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def oil_sump_and_inlet_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OilSumpAndInletTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rolling_bearing_element(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingBearingElement")

        if temp is None:
            return 0.0

        return temp

    @rolling_bearing_element.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_bearing_element(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RollingBearingElement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rolling_bearing_inner_race(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingBearingInnerRace")

        if temp is None:
            return 0.0

        return temp

    @rolling_bearing_inner_race.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_bearing_inner_race(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RollingBearingInnerRace",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def rolling_bearing_outer_race(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingBearingOuterRace")

        if temp is None:
            return 0.0

        return temp

    @rolling_bearing_outer_race.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_bearing_outer_race(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RollingBearingOuterRace",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Shaft")

        if temp is None:
            return 0.0

        return temp

    @shaft.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Shaft", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def temperature_when_assembled(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TemperatureWhenAssembled")

        if temp is None:
            return 0.0

        return temp

    @temperature_when_assembled.setter
    @exception_bridge
    @enforce_parameter_types
    def temperature_when_assembled(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TemperatureWhenAssembled",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_TransmissionTemperatureSet":
        """Cast to another type.

        Returns:
            _Cast_TransmissionTemperatureSet
        """
        return _Cast_TransmissionTemperatureSet(self)
