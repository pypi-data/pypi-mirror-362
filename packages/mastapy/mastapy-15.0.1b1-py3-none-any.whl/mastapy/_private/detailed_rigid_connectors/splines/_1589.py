"""PressureAngleTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PRESSURE_ANGLE_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "PressureAngleTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PressureAngleTypes")
    CastSelf = TypeVar("CastSelf", bound="PressureAngleTypes._Cast_PressureAngleTypes")


__docformat__ = "restructuredtext en"
__all__ = ("PressureAngleTypes",)


class PressureAngleTypes(Enum):
    """PressureAngleTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PRESSURE_ANGLE_TYPES

    _30 = 0
    _375 = 1
    _45 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PressureAngleTypes.__setattr__ = __enum_setattr
PressureAngleTypes.__delattr__ = __enum_delattr
