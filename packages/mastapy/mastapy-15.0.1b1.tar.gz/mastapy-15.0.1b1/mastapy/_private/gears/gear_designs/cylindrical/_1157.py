"""GearFitSystems"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_FIT_SYSTEMS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "GearFitSystems"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearFitSystems")
    CastSelf = TypeVar("CastSelf", bound="GearFitSystems._Cast_GearFitSystems")


__docformat__ = "restructuredtext en"
__all__ = ("GearFitSystems",)


class GearFitSystems(Enum):
    """GearFitSystems

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_FIT_SYSTEMS

    NONE = 0
    DIN_39671978 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearFitSystems.__setattr__ = __enum_setattr
GearFitSystems.__delattr__ = __enum_delattr
