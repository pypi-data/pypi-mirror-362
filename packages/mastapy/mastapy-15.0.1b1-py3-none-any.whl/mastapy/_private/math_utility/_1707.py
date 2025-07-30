"""PIDControlUpdateMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PID_CONTROL_UPDATE_METHOD = python_net_import(
    "SMT.MastaAPI.MathUtility", "PIDControlUpdateMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PIDControlUpdateMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="PIDControlUpdateMethod._Cast_PIDControlUpdateMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("PIDControlUpdateMethod",)


class PIDControlUpdateMethod(Enum):
    """PIDControlUpdateMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PID_CONTROL_UPDATE_METHOD

    EACH_SOLVER_STEP = 0
    SAMPLE_TIME = 1
    CONTINUOUS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PIDControlUpdateMethod.__setattr__ = __enum_setattr
PIDControlUpdateMethod.__delattr__ = __enum_delattr
