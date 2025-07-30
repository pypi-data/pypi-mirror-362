"""ElectricMachineAnalysisPeriod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELECTRIC_MACHINE_ANALYSIS_PERIOD = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "ElectricMachineAnalysisPeriod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineAnalysisPeriod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineAnalysisPeriod._Cast_ElectricMachineAnalysisPeriod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineAnalysisPeriod",)


class ElectricMachineAnalysisPeriod(Enum):
    """ElectricMachineAnalysisPeriod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELECTRIC_MACHINE_ANALYSIS_PERIOD

    ELECTRICAL_PERIOD = 0
    HALF_ELECTRICAL_PERIOD = 1
    MECHANICAL_PERIOD = 2
    SLOT_PASSING_PERIOD = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElectricMachineAnalysisPeriod.__setattr__ = __enum_setattr
ElectricMachineAnalysisPeriod.__delattr__ = __enum_delattr
