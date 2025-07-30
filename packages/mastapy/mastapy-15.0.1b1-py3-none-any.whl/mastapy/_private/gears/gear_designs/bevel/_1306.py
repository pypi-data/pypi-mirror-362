"""FinishingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FINISHING_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Bevel", "FinishingMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FinishingMethods")
    CastSelf = TypeVar("CastSelf", bound="FinishingMethods._Cast_FinishingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("FinishingMethods",)


class FinishingMethods(Enum):
    """FinishingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FINISHING_METHODS

    AS_CUT = 0
    CUT_AND_LAPPED = 1
    GROUND = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FinishingMethods.__setattr__ = __enum_setattr
FinishingMethods.__delattr__ = __enum_delattr
