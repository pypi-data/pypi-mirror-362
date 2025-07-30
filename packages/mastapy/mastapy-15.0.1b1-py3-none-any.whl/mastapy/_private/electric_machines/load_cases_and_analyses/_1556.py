"""SpecifyTorqueOrCurrent"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPECIFY_TORQUE_OR_CURRENT = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "SpecifyTorqueOrCurrent"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpecifyTorqueOrCurrent")
    CastSelf = TypeVar(
        "CastSelf", bound="SpecifyTorqueOrCurrent._Cast_SpecifyTorqueOrCurrent"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpecifyTorqueOrCurrent",)


class SpecifyTorqueOrCurrent(Enum):
    """SpecifyTorqueOrCurrent

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPECIFY_TORQUE_OR_CURRENT

    TARGET_TORQUE = 0
    MAXIMUM_TORQUE = 1
    CURRENT_AND_CURRENT_ANGLE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SpecifyTorqueOrCurrent.__setattr__ = __enum_setattr
SpecifyTorqueOrCurrent.__delattr__ = __enum_delattr
