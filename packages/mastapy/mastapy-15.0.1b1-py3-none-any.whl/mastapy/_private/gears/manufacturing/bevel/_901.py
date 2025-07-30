"""MachineTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MACHINE_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Bevel", "MachineTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MachineTypes")
    CastSelf = TypeVar("CastSelf", bound="MachineTypes._Cast_MachineTypes")


__docformat__ = "restructuredtext en"
__all__ = ("MachineTypes",)


class MachineTypes(Enum):
    """MachineTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MACHINE_TYPES

    CRADLE_STYLE = 0
    PHOENIX_STYLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MachineTypes.__setattr__ = __enum_setattr
MachineTypes.__delattr__ = __enum_delattr
