"""RollerEndShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROLLER_END_SHAPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollerEndShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerEndShape")
    CastSelf = TypeVar("CastSelf", bound="RollerEndShape._Cast_RollerEndShape")


__docformat__ = "restructuredtext en"
__all__ = ("RollerEndShape",)


class RollerEndShape(Enum):
    """RollerEndShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROLLER_END_SHAPE

    FLAT = 0
    DOMED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RollerEndShape.__setattr__ = __enum_setattr
RollerEndShape.__delattr__ = __enum_delattr
