"""TipReliefScuffingOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TIP_RELIEF_SCUFFING_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "TipReliefScuffingOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TipReliefScuffingOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="TipReliefScuffingOptions._Cast_TipReliefScuffingOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TipReliefScuffingOptions",)


class TipReliefScuffingOptions(Enum):
    """TipReliefScuffingOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TIP_RELIEF_SCUFFING_OPTIONS

    CALCULATE_USING_MICRO_GEOMETRY = 0
    CALCULATE_USING_MICRO_GEOMETRY_LIMIT_TO_OPTIMAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TipReliefScuffingOptions.__setattr__ = __enum_setattr
TipReliefScuffingOptions.__delattr__ = __enum_delattr
