"""SoundPressureEnclosureType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SOUND_PRESSURE_ENCLOSURE_TYPE = python_net_import(
    "SMT.MastaAPI.Materials", "SoundPressureEnclosureType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SoundPressureEnclosureType")
    CastSelf = TypeVar(
        "CastSelf", bound="SoundPressureEnclosureType._Cast_SoundPressureEnclosureType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SoundPressureEnclosureType",)


class SoundPressureEnclosureType(Enum):
    """SoundPressureEnclosureType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SOUND_PRESSURE_ENCLOSURE_TYPE

    FREE_FIELD = 0
    FREE_FIELD_OVER_REFLECTING_PLANE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SoundPressureEnclosureType.__setattr__ = __enum_setattr
SoundPressureEnclosureType.__delattr__ = __enum_delattr
