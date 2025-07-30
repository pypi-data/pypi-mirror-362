"""SpiralBevelToothTaper"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPIRAL_BEVEL_TOOTH_TAPER = python_net_import(
    "SMT.MastaAPI.Gears", "SpiralBevelToothTaper"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpiralBevelToothTaper")
    CastSelf = TypeVar(
        "CastSelf", bound="SpiralBevelToothTaper._Cast_SpiralBevelToothTaper"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpiralBevelToothTaper",)


class SpiralBevelToothTaper(Enum):
    """SpiralBevelToothTaper

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPIRAL_BEVEL_TOOTH_TAPER

    DUPLEX_DPLX = 0
    STANDARD_STD = 1
    TILTED_ROOT_LINE_TRL = 2
    USERSPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SpiralBevelToothTaper.__setattr__ = __enum_setattr
SpiralBevelToothTaper.__delattr__ = __enum_delattr
