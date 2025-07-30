"""PlanetaryDetail"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_PLANETARY_DETAIL = python_net_import("SMT.MastaAPI.Gears", "PlanetaryDetail")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _429

    Self = TypeVar("Self", bound="PlanetaryDetail")
    CastSelf = TypeVar("CastSelf", bound="PlanetaryDetail._Cast_PlanetaryDetail")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetaryDetail",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetaryDetail:
    """Special nested class for casting PlanetaryDetail to subclasses."""

    __parent__: "PlanetaryDetail"

    @property
    def planetary_detail(self: "CastSelf") -> "PlanetaryDetail":
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
class PlanetaryDetail(_0.APIBase):
    """PlanetaryDetail

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANETARY_DETAIL

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def first_planet_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstPlanetAngle")

        if temp is None:
            return 0.0

        return temp

    @first_planet_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_planet_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FirstPlanetAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def number_of_planets(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfPlanets")

        if temp is None:
            return 0

        return temp

    @number_of_planets.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_planets(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfPlanets", int(value) if value is not None else 0
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
    def regularly_spaced_planets(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "RegularlySpacedPlanets")

        if temp is None:
            return False

        return temp

    @regularly_spaced_planets.setter
    @exception_bridge
    @enforce_parameter_types
    def regularly_spaced_planets(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "RegularlySpacedPlanets",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def planet_delta_angles(self: "Self") -> "List[_429.NamedPlanetAngle]":
        """List[mastapy.gears.NamedPlanetAngle]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlanetDeltaAngles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetaryDetail":
        """Cast to another type.

        Returns:
            _Cast_PlanetaryDetail
        """
        return _Cast_PlanetaryDetail(self)
