"""SAETorqueCycles"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SAE_TORQUE_CYCLES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SAETorqueCycles"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SAETorqueCycles")
    CastSelf = TypeVar("CastSelf", bound="SAETorqueCycles._Cast_SAETorqueCycles")


__docformat__ = "restructuredtext en"
__all__ = ("SAETorqueCycles",)


class SAETorqueCycles(Enum):
    """SAETorqueCycles

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SAE_TORQUE_CYCLES

    _1000 = 3
    _10000 = 4
    _100000 = 5
    _1000000 = 6
    _10000000 = 7


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SAETorqueCycles.__setattr__ = __enum_setattr
SAETorqueCycles.__delattr__ = __enum_delattr
