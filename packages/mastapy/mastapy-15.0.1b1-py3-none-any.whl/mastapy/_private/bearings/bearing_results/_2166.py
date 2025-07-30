"""Orientations"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ORIENTATIONS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "Orientations"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="Orientations")
    CastSelf = TypeVar("CastSelf", bound="Orientations._Cast_Orientations")


__docformat__ = "restructuredtext en"
__all__ = ("Orientations",)


class Orientations(Enum):
    """Orientations

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ORIENTATIONS

    FLIPPED = 0
    DEFAULT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


Orientations.__setattr__ = __enum_setattr
Orientations.__delattr__ = __enum_delattr
