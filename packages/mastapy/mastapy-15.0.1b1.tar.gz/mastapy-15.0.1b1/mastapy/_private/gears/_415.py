"""GearFlanks"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_FLANKS = python_net_import("SMT.MastaAPI.Gears", "GearFlanks")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearFlanks")
    CastSelf = TypeVar("CastSelf", bound="GearFlanks._Cast_GearFlanks")


__docformat__ = "restructuredtext en"
__all__ = ("GearFlanks",)


class GearFlanks(Enum):
    """GearFlanks

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_FLANKS

    FLANK_A = 0
    FLANK_B = 1
    WORST = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearFlanks.__setattr__ = __enum_setattr
GearFlanks.__delattr__ = __enum_delattr
