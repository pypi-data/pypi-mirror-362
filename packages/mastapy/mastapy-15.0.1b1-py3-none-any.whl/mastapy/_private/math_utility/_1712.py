"""RotationAxis"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROTATION_AXIS = python_net_import("SMT.MastaAPI.MathUtility", "RotationAxis")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RotationAxis")
    CastSelf = TypeVar("CastSelf", bound="RotationAxis._Cast_RotationAxis")


__docformat__ = "restructuredtext en"
__all__ = ("RotationAxis",)


class RotationAxis(Enum):
    """RotationAxis

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROTATION_AXIS

    X_AXIS = 0
    Y_AXIS = 1
    Z_AXIS = 2
    USERSPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RotationAxis.__setattr__ = __enum_setattr
RotationAxis.__delattr__ = __enum_delattr
