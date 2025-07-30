"""AdvancedTimeSteppingAnalysisForModulationType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "AdvancedTimeSteppingAnalysisForModulationType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AdvancedTimeSteppingAnalysisForModulationType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AdvancedTimeSteppingAnalysisForModulationType._Cast_AdvancedTimeSteppingAnalysisForModulationType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AdvancedTimeSteppingAnalysisForModulationType",)


class AdvancedTimeSteppingAnalysisForModulationType(Enum):
    """AdvancedTimeSteppingAnalysisForModulationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION_TYPE

    QUASI_HARMONIC_ANALYSIS = 0
    SEPARATION_OF_TIMESCALES_TIME_STEPPING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AdvancedTimeSteppingAnalysisForModulationType.__setattr__ = __enum_setattr
AdvancedTimeSteppingAnalysisForModulationType.__delattr__ = __enum_delattr
