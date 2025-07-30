"""CentreDistanceChangeMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CENTRE_DISTANCE_CHANGE_METHOD = python_net_import(
    "SMT.MastaAPI.Gears", "CentreDistanceChangeMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CentreDistanceChangeMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="CentreDistanceChangeMethod._Cast_CentreDistanceChangeMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CentreDistanceChangeMethod",)


class CentreDistanceChangeMethod(Enum):
    """CentreDistanceChangeMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CENTRE_DISTANCE_CHANGE_METHOD

    AUTOMATIC = 0
    MANUAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CentreDistanceChangeMethod.__setattr__ = __enum_setattr
CentreDistanceChangeMethod.__delattr__ = __enum_delattr
