"""BearingRacePosition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_RACE_POSITION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "BearingRacePosition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingRacePosition")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingRacePosition._Cast_BearingRacePosition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingRacePosition",)


class BearingRacePosition(Enum):
    """BearingRacePosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_RACE_POSITION

    INNER = 0
    OUTER = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingRacePosition.__setattr__ = __enum_setattr
BearingRacePosition.__delattr__ = __enum_delattr
