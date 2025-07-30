"""BearingNodePosition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_NODE_POSITION = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Concept", "BearingNodePosition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingNodePosition")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingNodePosition._Cast_BearingNodePosition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingNodePosition",)


class BearingNodePosition(Enum):
    """BearingNodePosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_NODE_POSITION

    CENTRE = 0
    LEFT_AND_RIGHT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingNodePosition.__setattr__ = __enum_setattr
BearingNodePosition.__delattr__ = __enum_delattr
