"""PowerLoadInputTorqueSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_POWER_LOAD_INPUT_TORQUE_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel", "PowerLoadInputTorqueSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PowerLoadInputTorqueSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PowerLoadInputTorqueSpecificationMethod._Cast_PowerLoadInputTorqueSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PowerLoadInputTorqueSpecificationMethod",)


class PowerLoadInputTorqueSpecificationMethod(Enum):
    """PowerLoadInputTorqueSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _POWER_LOAD_INPUT_TORQUE_SPECIFICATION_METHOD

    CONSTANT_TORQUE = 0
    ELECTRIC_MACHINE_HARMONIC_LOAD_DATA = 1
    TORQUE_VS_TIME = 2
    ENGINE_SPEED_TORQUE_CURVE = 3
    PID_CONTROL = 4
    TORQUE_VS_ANGLE = 5
    TORQUE_VS_ANGLE_AND_SPEED = 6
    SPEED_VS_TIME = 7
    RUNUP_INPUT_LOAD = 8


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PowerLoadInputTorqueSpecificationMethod.__setattr__ = __enum_setattr
PowerLoadInputTorqueSpecificationMethod.__delattr__ = __enum_delattr
