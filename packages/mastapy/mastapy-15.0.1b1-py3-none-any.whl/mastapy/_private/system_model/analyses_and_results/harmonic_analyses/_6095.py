"""ResponseCacheLevel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RESPONSE_CACHE_LEVEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses", "ResponseCacheLevel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ResponseCacheLevel")
    CastSelf = TypeVar("CastSelf", bound="ResponseCacheLevel._Cast_ResponseCacheLevel")


__docformat__ = "restructuredtext en"
__all__ = ("ResponseCacheLevel",)


class ResponseCacheLevel(Enum):
    """ResponseCacheLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RESPONSE_CACHE_LEVEL

    FASTEST_CALCULATION = 0
    MEDIUM = 1
    LOWEST_MEMORY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ResponseCacheLevel.__setattr__ = __enum_setattr
ResponseCacheLevel.__delattr__ = __enum_delattr
