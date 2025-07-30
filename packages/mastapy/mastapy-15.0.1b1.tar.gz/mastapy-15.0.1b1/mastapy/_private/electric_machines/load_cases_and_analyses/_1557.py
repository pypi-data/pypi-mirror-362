"""SpeedPointsDistribution"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPEED_POINTS_DISTRIBUTION = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "SpeedPointsDistribution"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SpeedPointsDistribution")
    CastSelf = TypeVar(
        "CastSelf", bound="SpeedPointsDistribution._Cast_SpeedPointsDistribution"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SpeedPointsDistribution",)


class SpeedPointsDistribution(Enum):
    """SpeedPointsDistribution

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPEED_POINTS_DISTRIBUTION

    LINEAR = 0
    USERDEFINED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SpeedPointsDistribution.__setattr__ = __enum_setattr
SpeedPointsDistribution.__delattr__ = __enum_delattr
