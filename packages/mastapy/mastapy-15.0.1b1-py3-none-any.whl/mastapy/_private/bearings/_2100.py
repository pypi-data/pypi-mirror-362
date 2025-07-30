"""RotationalDirections"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROTATIONAL_DIRECTIONS = python_net_import(
    "SMT.MastaAPI.Bearings", "RotationalDirections"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotationalDirections")
    CastSelf = TypeVar(
        "CastSelf", bound="RotationalDirections._Cast_RotationalDirections"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotationalDirections",)


class RotationalDirections(Enum):
    """RotationalDirections

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROTATIONAL_DIRECTIONS

    CLOCKWISE = 0
    ANTICLOCKWISE = 1
    BIDIRECTIONAL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RotationalDirections.__setattr__ = __enum_setattr
RotationalDirections.__delattr__ = __enum_delattr
