"""MultipleExcitationsSpeedRangeOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MULTIPLE_EXCITATIONS_SPEED_RANGE_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses",
    "MultipleExcitationsSpeedRangeOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MultipleExcitationsSpeedRangeOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MultipleExcitationsSpeedRangeOption._Cast_MultipleExcitationsSpeedRangeOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MultipleExcitationsSpeedRangeOption",)


class MultipleExcitationsSpeedRangeOption(Enum):
    """MultipleExcitationsSpeedRangeOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MULTIPLE_EXCITATIONS_SPEED_RANGE_OPTION

    INTERSECTION_OF_SPEED_RANGES = 0
    UNION_OF_SPEED_RANGES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MultipleExcitationsSpeedRangeOption.__setattr__ = __enum_setattr
MultipleExcitationsSpeedRangeOption.__delattr__ = __enum_delattr
