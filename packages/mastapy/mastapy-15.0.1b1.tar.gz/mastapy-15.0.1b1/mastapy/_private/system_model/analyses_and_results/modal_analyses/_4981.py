"""WhineWaterfallExportOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_WHINE_WATERFALL_EXPORT_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "WhineWaterfallExportOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="WhineWaterfallExportOption")
    CastSelf = TypeVar(
        "CastSelf", bound="WhineWaterfallExportOption._Cast_WhineWaterfallExportOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("WhineWaterfallExportOption",)


class WhineWaterfallExportOption(Enum):
    """WhineWaterfallExportOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _WHINE_WATERFALL_EXPORT_OPTION

    MATRIX = 0
    POINTS_LIST = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


WhineWaterfallExportOption.__setattr__ = __enum_setattr
WhineWaterfallExportOption.__delattr__ = __enum_delattr
