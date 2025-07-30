"""HardnessType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HARDNESS_TYPE = python_net_import("SMT.MastaAPI.Materials", "HardnessType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HardnessType")
    CastSelf = TypeVar("CastSelf", bound="HardnessType._Cast_HardnessType")


__docformat__ = "restructuredtext en"
__all__ = ("HardnessType",)


class HardnessType(Enum):
    """HardnessType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HARDNESS_TYPE

    BRINELL_3000KG_HB = 0
    VICKERS_HV = 1
    ROCKWELL_C_HRC = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HardnessType.__setattr__ = __enum_setattr
HardnessType.__delattr__ = __enum_delattr
