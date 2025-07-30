"""RollingBearingRaceType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROLLING_BEARING_RACE_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings", "RollingBearingRaceType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollingBearingRaceType")
    CastSelf = TypeVar(
        "CastSelf", bound="RollingBearingRaceType._Cast_RollingBearingRaceType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearingRaceType",)


class RollingBearingRaceType(Enum):
    """RollingBearingRaceType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROLLING_BEARING_RACE_TYPE

    NONE = 0
    DRAWN = 1
    MACHINED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RollingBearingRaceType.__setattr__ = __enum_setattr
RollingBearingRaceType.__delattr__ = __enum_delattr
