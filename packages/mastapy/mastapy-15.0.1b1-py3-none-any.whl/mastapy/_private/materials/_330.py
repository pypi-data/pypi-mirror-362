"""AirProperties"""

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

_AIR_PROPERTIES = python_net_import("SMT.MastaAPI.Materials", "AirProperties")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AirProperties")
    CastSelf = TypeVar("CastSelf", bound="AirProperties._Cast_AirProperties")


__docformat__ = "restructuredtext en"
__all__ = ("AirProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_AirProperties:
    """Special nested class for casting AirProperties to subclasses."""

    __parent__: "AirProperties"

    @property
    def air_properties(self: "CastSelf") -> "AirProperties":
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
class AirProperties(_0.APIBase):
    """AirProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _AIR_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adiabatic_index(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AdiabaticIndex")

        if temp is None:
            return 0.0

        return temp

    @adiabatic_index.setter
    @exception_bridge
    @enforce_parameter_types
    def adiabatic_index(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "AdiabaticIndex", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Pressure")

        if temp is None:
            return 0.0

        return temp

    @pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Pressure", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def specific_gas_constant(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecificGasConstant")

        if temp is None:
            return 0.0

        return temp

    @specific_gas_constant.setter
    @exception_bridge
    @enforce_parameter_types
    def specific_gas_constant(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecificGasConstant",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_AirProperties":
        """Cast to another type.

        Returns:
            _Cast_AirProperties
        """
        return _Cast_AirProperties(self)
