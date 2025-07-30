"""ConicalMeshedWheelFlankManufacturingConfig"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import python_net_import
from mastapy._private.gears import _409

_CONICAL_MESHED_WHEEL_FLANK_MANUFACTURING_CONFIG = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel",
    "ConicalMeshedWheelFlankManufacturingConfig",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalMeshedWheelFlankManufacturingConfig")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ConicalMeshedWheelFlankManufacturingConfig._Cast_ConicalMeshedWheelFlankManufacturingConfig",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalMeshedWheelFlankManufacturingConfig",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ConicalMeshedWheelFlankManufacturingConfig:
    """Special nested class for casting ConicalMeshedWheelFlankManufacturingConfig to subclasses."""

    __parent__: "ConicalMeshedWheelFlankManufacturingConfig"

    @property
    def conical_gear_tooth_surface(self: "CastSelf") -> "_409.ConicalGearToothSurface":
        return self.__parent__._cast(_409.ConicalGearToothSurface)

    @property
    def conical_meshed_wheel_flank_manufacturing_config(
        self: "CastSelf",
    ) -> "ConicalMeshedWheelFlankManufacturingConfig":
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
class ConicalMeshedWheelFlankManufacturingConfig(_409.ConicalGearToothSurface):
    """ConicalMeshedWheelFlankManufacturingConfig

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CONICAL_MESHED_WHEEL_FLANK_MANUFACTURING_CONFIG

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    def cast_to(self: "Self") -> "_Cast_ConicalMeshedWheelFlankManufacturingConfig":
        """Cast to another type.

        Returns:
            _Cast_ConicalMeshedWheelFlankManufacturingConfig
        """
        return _Cast_ConicalMeshedWheelFlankManufacturingConfig(self)
