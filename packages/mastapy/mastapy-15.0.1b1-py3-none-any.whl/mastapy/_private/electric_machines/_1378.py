"""CoolingChannelShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COOLING_CHANNEL_SHAPE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CoolingChannelShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoolingChannelShape")
    CastSelf = TypeVar(
        "CastSelf", bound="CoolingChannelShape._Cast_CoolingChannelShape"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoolingChannelShape",)


class CoolingChannelShape(Enum):
    """CoolingChannelShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COOLING_CHANNEL_SHAPE

    RECTANGLE = 0
    CIRCLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoolingChannelShape.__setattr__ = __enum_setattr
CoolingChannelShape.__delattr__ = __enum_delattr
