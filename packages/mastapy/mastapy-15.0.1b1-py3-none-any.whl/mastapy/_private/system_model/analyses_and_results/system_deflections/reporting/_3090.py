"""PlanetPinWindup"""

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
)

_PLANET_PIN_WINDUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "PlanetPinWindup",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlanetPinWindup")
    CastSelf = TypeVar("CastSelf", bound="PlanetPinWindup._Cast_PlanetPinWindup")


__docformat__ = "restructuredtext en"
__all__ = ("PlanetPinWindup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetPinWindup:
    """Special nested class for casting PlanetPinWindup to subclasses."""

    __parent__: "PlanetPinWindup"

    @property
    def planet_pin_windup(self: "CastSelf") -> "PlanetPinWindup":
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
class PlanetPinWindup(_0.APIBase):
    """PlanetPinWindup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_PIN_WINDUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Angle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radial_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadialTilt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_axial_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeAxialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_radial_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeRadialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_tangential_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeTangentialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tangential_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TangentialTilt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_wind_up(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalWindUp")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetPinWindup":
        """Cast to another type.

        Returns:
            _Cast_PlanetPinWindup
        """
        return _Cast_PlanetPinWindup(self)
