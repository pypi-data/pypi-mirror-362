"""Flank"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLANK = python_net_import("SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "Flank")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Flank")
    CastSelf = TypeVar("CastSelf", bound="Flank._Cast_Flank")


__docformat__ = "restructuredtext en"
__all__ = ("Flank",)


class Flank(Enum):
    """Flank

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLANK

    LEFT_FLANK = 0
    RIGHT_FLANK = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Flank.__setattr__ = __enum_setattr
Flank.__delattr__ = __enum_delattr
