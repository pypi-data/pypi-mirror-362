"""FluidFilmTemperatureOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLUID_FILM_TEMPERATURE_OPTIONS = python_net_import(
    "SMT.MastaAPI.Bearings", "FluidFilmTemperatureOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FluidFilmTemperatureOptions")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FluidFilmTemperatureOptions._Cast_FluidFilmTemperatureOptions",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FluidFilmTemperatureOptions",)


class FluidFilmTemperatureOptions(Enum):
    """FluidFilmTemperatureOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLUID_FILM_TEMPERATURE_OPTIONS

    CALCULATE_USING_DIN_7322010_WHERE_AVAILABLE = 0
    CALCULATE_FROM_SPECIFIED_ELEMENT_AND_RING_TEMPERATURES = 1
    USE_SPECIFIED_ELEMENT_TEMPERATURE = 2
    USE_SPECIFIED_SUMP_TEMPERATURE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FluidFilmTemperatureOptions.__setattr__ = __enum_setattr
FluidFilmTemperatureOptions.__delattr__ = __enum_delattr
