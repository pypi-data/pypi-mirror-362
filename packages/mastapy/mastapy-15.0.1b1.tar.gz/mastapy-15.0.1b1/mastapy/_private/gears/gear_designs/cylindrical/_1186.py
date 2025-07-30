"""ScuffingTemperatureMethodsISO"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SCUFFING_TEMPERATURE_METHODS_ISO = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ScuffingTemperatureMethodsISO"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ScuffingTemperatureMethodsISO")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ScuffingTemperatureMethodsISO._Cast_ScuffingTemperatureMethodsISO",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ScuffingTemperatureMethodsISO",)


class ScuffingTemperatureMethodsISO(Enum):
    """ScuffingTemperatureMethodsISO

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SCUFFING_TEMPERATURE_METHODS_ISO

    USER_INPUT = 0
    USER_INPUT_SCUFFING_TEMPERATURE_AT_LONG_CONTACT_TIMES = 1
    USER_INPUT_FZG_LOAD_STAGE = 2
    ESTIMATED_FROM_TEST_GEARS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ScuffingTemperatureMethodsISO.__setattr__ = __enum_setattr
ScuffingTemperatureMethodsISO.__delattr__ = __enum_delattr
