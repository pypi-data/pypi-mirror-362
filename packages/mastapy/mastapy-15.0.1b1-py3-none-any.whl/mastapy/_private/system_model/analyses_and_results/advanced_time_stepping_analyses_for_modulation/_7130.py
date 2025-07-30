"""AtsamNaturalFrequencyViewOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ATSAM_NATURAL_FREQUENCY_VIEW_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "AtsamNaturalFrequencyViewOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AtsamNaturalFrequencyViewOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AtsamNaturalFrequencyViewOption._Cast_AtsamNaturalFrequencyViewOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AtsamNaturalFrequencyViewOption",)


class AtsamNaturalFrequencyViewOption(Enum):
    """AtsamNaturalFrequencyViewOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ATSAM_NATURAL_FREQUENCY_VIEW_OPTION

    ALL_MODES_AT_SELECTED_LARGE_TIME_STEP = 0
    RANGE_OF_SELECTED_MODE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AtsamNaturalFrequencyViewOption.__setattr__ = __enum_setattr
AtsamNaturalFrequencyViewOption.__delattr__ = __enum_delattr
