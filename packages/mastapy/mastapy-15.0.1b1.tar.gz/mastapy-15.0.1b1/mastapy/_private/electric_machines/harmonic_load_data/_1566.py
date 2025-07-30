"""HarmonicLoadDataType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HARMONIC_LOAD_DATA_TYPE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "HarmonicLoadDataType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicLoadDataType")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicLoadDataType._Cast_HarmonicLoadDataType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicLoadDataType",)


class HarmonicLoadDataType(Enum):
    """HarmonicLoadDataType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HARMONIC_LOAD_DATA_TYPE

    TE = 0
    MISALIGNMENT = 1
    ROTOR_TORQUE_RIPPLE = 2
    SPEED_INDEPENDENT_FORCE = 3
    SPEED_DEPENDENT_FORCE = 4
    STATOR_TEETH_RADIAL_LOADS = 5
    STATOR_TEETH_TANGENTIAL_LOADS = 6
    ROTOR_XFORCES = 7
    ROTOR_YFORCES = 8
    ROTOR_ZFORCES = 9
    ROTOR_XMOMENT = 10
    ROTOR_YMOMENT = 11
    STATOR_TEETH_AXIAL_LOADS = 12
    STATOR_TEETH_MOMENTS = 13


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HarmonicLoadDataType.__setattr__ = __enum_setattr
HarmonicLoadDataType.__delattr__ = __enum_delattr
