"""CriticalSpeed"""

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

_CRITICAL_SPEED = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StabilityAnalyses", "CriticalSpeed"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CriticalSpeed")
    CastSelf = TypeVar("CastSelf", bound="CriticalSpeed._Cast_CriticalSpeed")


__docformat__ = "restructuredtext en"
__all__ = ("CriticalSpeed",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CriticalSpeed:
    """Special nested class for casting CriticalSpeed to subclasses."""

    __parent__: "CriticalSpeed"

    @property
    def critical_speed(self: "CastSelf") -> "CriticalSpeed":
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
class CriticalSpeed(_0.APIBase):
    """CriticalSpeed

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CRITICAL_SPEED

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def critical_speed_as_frequency(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAsFrequency")

        if temp is None:
            return 0.0

        return temp

    @critical_speed_as_frequency.setter
    @exception_bridge
    @enforce_parameter_types
    def critical_speed_as_frequency(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CriticalSpeedAsFrequency",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def critical_speed_as_shaft_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CriticalSpeedAsShaftSpeed")

        if temp is None:
            return 0.0

        return temp

    @critical_speed_as_shaft_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def critical_speed_as_shaft_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CriticalSpeedAsShaftSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def mode_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ModeIndex")

        if temp is None:
            return 0

        return temp

    @mode_index.setter
    @exception_bridge
    @enforce_parameter_types
    def mode_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ModeIndex", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def shaft_harmonic_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ShaftHarmonicIndex")

        if temp is None:
            return 0

        return temp

    @shaft_harmonic_index.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_harmonic_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftHarmonicIndex", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CriticalSpeed":
        """Cast to another type.

        Returns:
            _Cast_CriticalSpeed
        """
        return _Cast_CriticalSpeed(self)
