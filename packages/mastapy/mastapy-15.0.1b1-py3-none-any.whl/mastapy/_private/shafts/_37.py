"""ShaftRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHAFT_RATING_METHOD = python_net_import("SMT.MastaAPI.Shafts", "ShaftRatingMethod")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftRatingMethod")
    CastSelf = TypeVar("CastSelf", bound="ShaftRatingMethod._Cast_ShaftRatingMethod")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftRatingMethod",)


class ShaftRatingMethod(Enum):
    """ShaftRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHAFT_RATING_METHOD

    DIN_743201212 = 0
    SMT = 1
    AGMA_60016101E08 = 2
    FKM_GUIDELINE_6TH_EDITION_2012 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShaftRatingMethod.__setattr__ = __enum_setattr
ShaftRatingMethod.__delattr__ = __enum_delattr
