"""SpiralBevelRateableGear"""

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

_SPIRAL_BEVEL_RATEABLE_GEAR = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Bevel.Standards", "SpiralBevelRateableGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpiralBevelRateableGear")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelRateableGear._Cast_SpiralBevelRateableGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelRateableGear",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SpiralBevelRateableGear:
    """Special nested class for casting SpiralBevelRateableGear to subclasses."""

    __parent__: "SpiralBevelRateableGear"

    @property
    def spiral_bevel_rateable_gear(self: "CastSelf") -> "SpiralBevelRateableGear":
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
class SpiralBevelRateableGear(_0.APIBase):
    """SpiralBevelRateableGear

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPIRAL_BEVEL_RATEABLE_GEAR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def gear_blank_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearBlankTemperature")

        if temp is None:
            return 0.0

        return temp

    @gear_blank_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_blank_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearBlankTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SpiralBevelRateableGear":
        """Cast to another type.

        Returns:
            _Cast_SpiralBevelRateableGear
        """
        return _Cast_SpiralBevelRateableGear(self)
