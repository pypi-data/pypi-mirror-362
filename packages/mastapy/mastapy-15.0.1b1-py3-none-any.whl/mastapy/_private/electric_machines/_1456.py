"""WindingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WINDING_TYPE = python_net_import("SMT.MastaAPI.ElectricMachines", "WindingType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WindingType")
    CastSelf = TypeVar("CastSelf", bound="WindingType._Cast_WindingType")


__docformat__ = "restructuredtext en"
__all__ = ("WindingType",)


class WindingType(Enum):
    """WindingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WINDING_TYPE

    ROUND_CONDUCTORS = 0
    HAIRPIN = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WindingType.__setattr__ = __enum_setattr
WindingType.__delattr__ = __enum_delattr
