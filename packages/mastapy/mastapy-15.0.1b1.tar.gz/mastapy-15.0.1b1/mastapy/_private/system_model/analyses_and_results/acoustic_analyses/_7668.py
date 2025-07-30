"""NearFieldIntegralsCacheType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NEAR_FIELD_INTEGRALS_CACHE_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "NearFieldIntegralsCacheType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NearFieldIntegralsCacheType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="NearFieldIntegralsCacheType._Cast_NearFieldIntegralsCacheType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("NearFieldIntegralsCacheType",)


class NearFieldIntegralsCacheType(Enum):
    """NearFieldIntegralsCacheType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NEAR_FIELD_INTEGRALS_CACHE_TYPE

    NONE = 0
    SINGLE_CELL = 1
    ADJACENT_CELLS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NearFieldIntegralsCacheType.__setattr__ = __enum_setattr
NearFieldIntegralsCacheType.__delattr__ = __enum_delattr
