"""DynamicsResponseScaling"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DYNAMICS_RESPONSE_SCALING = python_net_import(
    "SMT.MastaAPI.MathUtility", "DynamicsResponseScaling"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DynamicsResponseScaling")
    CastSelf = TypeVar(
        "CastSelf", bound="DynamicsResponseScaling._Cast_DynamicsResponseScaling"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DynamicsResponseScaling",)


class DynamicsResponseScaling(Enum):
    """DynamicsResponseScaling

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DYNAMICS_RESPONSE_SCALING

    NO_SCALING = 0
    LOG_BASE_10 = 1
    DECIBEL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DynamicsResponseScaling.__setattr__ = __enum_setattr
DynamicsResponseScaling.__delattr__ = __enum_delattr
