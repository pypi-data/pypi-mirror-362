"""M2LHfCacheType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_M2L_HF_CACHE_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses", "M2LHfCacheType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="M2LHfCacheType")
    CastSelf = TypeVar("CastSelf", bound="M2LHfCacheType._Cast_M2LHfCacheType")


__docformat__ = "restructuredtext en"
__all__ = ("M2LHfCacheType",)


class M2LHfCacheType(Enum):
    """M2LHfCacheType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _M2L_HF_CACHE_TYPE

    NONE = 0
    ALL_CELLS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


M2LHfCacheType.__setattr__ = __enum_setattr
M2LHfCacheType.__delattr__ = __enum_delattr
