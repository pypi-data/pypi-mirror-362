"""PowerLoadPIDControlSpeedInputType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_POWER_LOAD_PID_CONTROL_SPEED_INPUT_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel", "PowerLoadPIDControlSpeedInputType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerLoadPIDControlSpeedInputType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerLoadPIDControlSpeedInputType._Cast_PowerLoadPIDControlSpeedInputType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadPIDControlSpeedInputType",)


class PowerLoadPIDControlSpeedInputType(Enum):
    """PowerLoadPIDControlSpeedInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _POWER_LOAD_PID_CONTROL_SPEED_INPUT_TYPE

    CONSTANT_SPEED = 0
    SPEED_VS_TIME = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PowerLoadPIDControlSpeedInputType.__setattr__ = __enum_setattr
PowerLoadPIDControlSpeedInputType.__delattr__ = __enum_delattr
