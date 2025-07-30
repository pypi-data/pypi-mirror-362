"""ZerolBevelGleasonToothTaperOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ZEROL_BEVEL_GLEASON_TOOTH_TAPER_OPTION = python_net_import(
    "SMT.MastaAPI.Gears", "ZerolBevelGleasonToothTaperOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ZerolBevelGleasonToothTaperOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ZerolBevelGleasonToothTaperOption._Cast_ZerolBevelGleasonToothTaperOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ZerolBevelGleasonToothTaperOption",)


class ZerolBevelGleasonToothTaperOption(Enum):
    """ZerolBevelGleasonToothTaperOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ZEROL_BEVEL_GLEASON_TOOTH_TAPER_OPTION

    DUPLEX_OLD = 0
    FINE_PITCH_ZEROL = 1
    COARSE_PITCH_ZEROL = 2
    USERSPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ZerolBevelGleasonToothTaperOption.__setattr__ = __enum_setattr
ZerolBevelGleasonToothTaperOption.__delattr__ = __enum_delattr
