"""ScuffingFlashTemperatureRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SCUFFING_FLASH_TEMPERATURE_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ScuffingFlashTemperatureRatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ScuffingFlashTemperatureRatingMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ScuffingFlashTemperatureRatingMethod._Cast_ScuffingFlashTemperatureRatingMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ScuffingFlashTemperatureRatingMethod",)


class ScuffingFlashTemperatureRatingMethod(Enum):
    """ScuffingFlashTemperatureRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SCUFFING_FLASH_TEMPERATURE_RATING_METHOD

    ISOTR_1398912000 = 0
    ISOTS_6336202017 = 1
    ISOTS_6336202022 = 2
    DIN_399041987 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ScuffingFlashTemperatureRatingMethod.__setattr__ = __enum_setattr
ScuffingFlashTemperatureRatingMethod.__delattr__ = __enum_delattr
