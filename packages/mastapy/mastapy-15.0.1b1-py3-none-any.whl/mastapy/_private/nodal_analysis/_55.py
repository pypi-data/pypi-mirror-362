"""BarModelAnalysisType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BAR_MODEL_ANALYSIS_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "BarModelAnalysisType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BarModelAnalysisType")
    CastSelf = TypeVar(
        "CastSelf", bound="BarModelAnalysisType._Cast_BarModelAnalysisType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BarModelAnalysisType",)


class BarModelAnalysisType(Enum):
    """BarModelAnalysisType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BAR_MODEL_ANALYSIS_TYPE

    STATIC = 0
    DYNAMIC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BarModelAnalysisType.__setattr__ = __enum_setattr
BarModelAnalysisType.__delattr__ = __enum_delattr
