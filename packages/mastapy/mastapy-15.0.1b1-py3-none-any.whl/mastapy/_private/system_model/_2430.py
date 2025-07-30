"""PowerLoadType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_POWER_LOAD_TYPE = python_net_import("SMT.MastaAPI.SystemModel", "PowerLoadType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerLoadType")
    CastSelf = TypeVar("CastSelf", bound="PowerLoadType._Cast_PowerLoadType")


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadType",)


class PowerLoadType(Enum):
    """PowerLoadType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _POWER_LOAD_TYPE

    BASIC = 0
    WIND_TURBINE_BLADES = 1
    ENGINE = 2
    ELECTRIC_MACHINE = 3
    WHEELS = 4
    OIL_PUMP = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PowerLoadType.__setattr__ = __enum_setattr
PowerLoadType.__delattr__ = __enum_delattr
