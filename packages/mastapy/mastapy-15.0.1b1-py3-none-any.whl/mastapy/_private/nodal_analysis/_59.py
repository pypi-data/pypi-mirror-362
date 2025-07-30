"""DampingScalingTypeForInitialTransients"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DAMPING_SCALING_TYPE_FOR_INITIAL_TRANSIENTS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "DampingScalingTypeForInitialTransients"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DampingScalingTypeForInitialTransients")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DampingScalingTypeForInitialTransients._Cast_DampingScalingTypeForInitialTransients",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DampingScalingTypeForInitialTransients",)


class DampingScalingTypeForInitialTransients(Enum):
    """DampingScalingTypeForInitialTransients

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DAMPING_SCALING_TYPE_FOR_INITIAL_TRANSIENTS

    NONE = 0
    LINEAR = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DampingScalingTypeForInitialTransients.__setattr__ = __enum_setattr
DampingScalingTypeForInitialTransients.__delattr__ = __enum_delattr
