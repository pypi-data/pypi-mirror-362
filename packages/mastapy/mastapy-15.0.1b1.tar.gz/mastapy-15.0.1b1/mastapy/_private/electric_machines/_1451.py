"""WindingConnection"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WINDING_CONNECTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "WindingConnection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WindingConnection")
    CastSelf = TypeVar("CastSelf", bound="WindingConnection._Cast_WindingConnection")


__docformat__ = "restructuredtext en"
__all__ = ("WindingConnection",)


class WindingConnection(Enum):
    """WindingConnection

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WINDING_CONNECTION

    STAR_CONNECTION = 0
    DELTA_CONNECTION = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WindingConnection.__setattr__ = __enum_setattr
WindingConnection.__delattr__ = __enum_delattr
