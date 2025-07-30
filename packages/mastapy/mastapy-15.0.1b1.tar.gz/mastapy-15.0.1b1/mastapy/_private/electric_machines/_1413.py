"""MagnetConfiguration"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MAGNET_CONFIGURATION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "MagnetConfiguration"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MagnetConfiguration")
    CastSelf = TypeVar(
        "CastSelf", bound="MagnetConfiguration._Cast_MagnetConfiguration"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MagnetConfiguration",)


class MagnetConfiguration(Enum):
    """MagnetConfiguration

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MAGNET_CONFIGURATION

    NO_MAGNETS = 0
    INNER_MAGNETS_ONLY = 1
    OUTER_MAGNETS_ONLY = 2
    INNER_AND_OUTER_MAGNETS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MagnetConfiguration.__setattr__ = __enum_setattr
MagnetConfiguration.__delattr__ = __enum_delattr
