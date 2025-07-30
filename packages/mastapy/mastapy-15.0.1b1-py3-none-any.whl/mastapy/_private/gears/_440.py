"""WormAddendumFactor"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WORM_ADDENDUM_FACTOR = python_net_import("SMT.MastaAPI.Gears", "WormAddendumFactor")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WormAddendumFactor")
    CastSelf = TypeVar("CastSelf", bound="WormAddendumFactor._Cast_WormAddendumFactor")


__docformat__ = "restructuredtext en"
__all__ = ("WormAddendumFactor",)


class WormAddendumFactor(Enum):
    """WormAddendumFactor

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WORM_ADDENDUM_FACTOR

    NORMAL = 0
    STUB = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WormAddendumFactor.__setattr__ = __enum_setattr
WormAddendumFactor.__delattr__ = __enum_delattr
