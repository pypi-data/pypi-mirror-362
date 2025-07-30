"""MagnetisationDirection"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MAGNETISATION_DIRECTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "MagnetisationDirection"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MagnetisationDirection")
    CastSelf = TypeVar(
        "CastSelf", bound="MagnetisationDirection._Cast_MagnetisationDirection"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MagnetisationDirection",)


class MagnetisationDirection(Enum):
    """MagnetisationDirection

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MAGNETISATION_DIRECTION

    AS_CALCULATED = 0
    PLUS_90_FROM_CALCULATED = 1
    MINUS_90_FROM_CALCULATED = 2
    PLUS_180_FROM_CALCULATED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MagnetisationDirection.__setattr__ = __enum_setattr
MagnetisationDirection.__delattr__ = __enum_delattr
