"""PlanetCarrierWindup"""

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
)

_PLANET_CARRIER_WINDUP = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections.Reporting",
    "PlanetCarrierWindup",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3090,
    )

    Self = TypeVar("Self", bound="PlanetCarrierWindup")
    CastSelf = TypeVar(
        "CastSelf", bound="PlanetCarrierWindup._Cast_PlanetCarrierWindup"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetCarrierWindup",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlanetCarrierWindup:
    """Special nested class for casting PlanetCarrierWindup to subclasses."""

    __parent__: "PlanetCarrierWindup"

    @property
    def planet_carrier_windup(self: "CastSelf") -> "PlanetCarrierWindup":
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
class PlanetCarrierWindup(_0.APIBase):
    """PlanetCarrierWindup

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLANET_CARRIER_WINDUP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def average_axial_deflection(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageAxialDeflection")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_radial_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageRadialTilt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_tangential_tilt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageTangentialTilt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_torsional_wind_up(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageTorsionalWindUp")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def other_planet_carrier(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OtherPlanetCarrier")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def other_socket(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OtherSocket")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def reference_socket(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReferenceSocket")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def pin_wind_ups(self: "Self") -> "List[_3090.PlanetPinWindup]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.PlanetPinWindup]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinWindUps")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_PlanetCarrierWindup":
        """Cast to another type.

        Returns:
            _Cast_PlanetCarrierWindup
        """
        return _Cast_PlanetCarrierWindup(self)
