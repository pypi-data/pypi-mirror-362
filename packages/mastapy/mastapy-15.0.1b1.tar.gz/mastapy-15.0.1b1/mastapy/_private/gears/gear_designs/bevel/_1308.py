"""PrimeMoverCharacteristicGleason"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PRIME_MOVER_CHARACTERISTIC_GLEASON = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "PrimeMoverCharacteristicGleason"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PrimeMoverCharacteristicGleason")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PrimeMoverCharacteristicGleason._Cast_PrimeMoverCharacteristicGleason",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PrimeMoverCharacteristicGleason",)


class PrimeMoverCharacteristicGleason(Enum):
    """PrimeMoverCharacteristicGleason

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PRIME_MOVER_CHARACTERISTIC_GLEASON

    UNIFORM = 0
    LIGHT_SHOCK = 1
    MEDIUM_SHOCK = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PrimeMoverCharacteristicGleason.__setattr__ = __enum_setattr
PrimeMoverCharacteristicGleason.__delattr__ = __enum_delattr
