"""ScuffingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SCUFFING_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "ScuffingMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ScuffingMethods")
    CastSelf = TypeVar("CastSelf", bound="ScuffingMethods._Cast_ScuffingMethods")


__docformat__ = "restructuredtext en"
__all__ = ("ScuffingMethods",)


class ScuffingMethods(Enum):
    """ScuffingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SCUFFING_METHODS

    AGMA_2001B88 = 0
    AGMA_925A03 = 1
    AGMA_925B22 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ScuffingMethods.__setattr__ = __enum_setattr
ScuffingMethods.__delattr__ = __enum_delattr
