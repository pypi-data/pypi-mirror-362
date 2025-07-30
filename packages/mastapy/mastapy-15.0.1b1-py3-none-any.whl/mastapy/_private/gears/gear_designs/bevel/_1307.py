"""MachineCharacteristicAGMAKlingelnberg"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MACHINE_CHARACTERISTIC_AGMA_KLINGELNBERG = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "MachineCharacteristicAGMAKlingelnberg"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MachineCharacteristicAGMAKlingelnberg")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MachineCharacteristicAGMAKlingelnberg._Cast_MachineCharacteristicAGMAKlingelnberg",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MachineCharacteristicAGMAKlingelnberg",)


class MachineCharacteristicAGMAKlingelnberg(Enum):
    """MachineCharacteristicAGMAKlingelnberg

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MACHINE_CHARACTERISTIC_AGMA_KLINGELNBERG

    UNIFORM = 0
    LIGHT_SHOCK = 1
    MEDIUM_SHOCK = 2
    HEAVY_SHOCK = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MachineCharacteristicAGMAKlingelnberg.__setattr__ = __enum_setattr
MachineCharacteristicAGMAKlingelnberg.__delattr__ = __enum_delattr
