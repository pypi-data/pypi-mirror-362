"""PlanetGearOptions"""

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

_PLANET_GEAR_OPTIONS = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization.SystemOptimiser", "PlanetGearOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlanetGearOptions")
    CastSelf = TypeVar("CastSelf", bound="PlanetGearOptions._Cast_PlanetGearOptions")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetGearOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetGearOptions:
    """Special nested class for casting PlanetGearOptions to subclasses."""

    __parent__: "PlanetGearOptions"

    @property
    def planet_gear_options(self: "CastSelf") -> "PlanetGearOptions":
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
class PlanetGearOptions(_0.APIBase):
    """PlanetGearOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_GEAR_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def cast_to(self: "Self") -> "_Cast_PlanetGearOptions":
        """Cast to another type.

        Returns:
            _Cast_PlanetGearOptions
        """
        return _Cast_PlanetGearOptions(self)
