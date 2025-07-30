"""OuterRingMounting"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OUTER_RING_MOUNTING = python_net_import("SMT.MastaAPI.Bearings", "OuterRingMounting")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OuterRingMounting")
    CastSelf = TypeVar("CastSelf", bound="OuterRingMounting._Cast_OuterRingMounting")


__docformat__ = "restructuredtext en"
__all__ = ("OuterRingMounting",)


class OuterRingMounting(Enum):
    """OuterRingMounting

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OUTER_RING_MOUNTING

    STANDARD = 0
    SPHERICAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OuterRingMounting.__setattr__ = __enum_setattr
OuterRingMounting.__delattr__ = __enum_delattr
