"""CageBridgeShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CAGE_BRIDGE_SHAPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "CageBridgeShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CageBridgeShape")
    CastSelf = TypeVar("CastSelf", bound="CageBridgeShape._Cast_CageBridgeShape")


__docformat__ = "restructuredtext en"
__all__ = ("CageBridgeShape",)


class CageBridgeShape(Enum):
    """CageBridgeShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CAGE_BRIDGE_SHAPE

    FLAT = 0
    CURVED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CageBridgeShape.__setattr__ = __enum_setattr
CageBridgeShape.__delattr__ = __enum_delattr
