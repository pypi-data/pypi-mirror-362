"""BearingEfficiencyRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_EFFICIENCY_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "BearingEfficiencyRatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingEfficiencyRatingMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="BearingEfficiencyRatingMethod._Cast_BearingEfficiencyRatingMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingEfficiencyRatingMethod",)


class BearingEfficiencyRatingMethod(Enum):
    """BearingEfficiencyRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_EFFICIENCY_RATING_METHOD

    ISOTR_1417912001 = 0
    ISOTR_1417922001 = 1
    SKF_LOSS_MODEL = 2
    SMT_ADVANCED_MODEL = 3
    SCRIPT = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingEfficiencyRatingMethod.__setattr__ = __enum_setattr
BearingEfficiencyRatingMethod.__delattr__ = __enum_delattr
