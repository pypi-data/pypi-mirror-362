"""InertiaAdjustedLoadCasePeriodMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INERTIA_ADJUSTED_LOAD_CASE_PERIOD_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "InertiaAdjustedLoadCasePeriodMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InertiaAdjustedLoadCasePeriodMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="InertiaAdjustedLoadCasePeriodMethod._Cast_InertiaAdjustedLoadCasePeriodMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("InertiaAdjustedLoadCasePeriodMethod",)


class InertiaAdjustedLoadCasePeriodMethod(Enum):
    """InertiaAdjustedLoadCasePeriodMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INERTIA_ADJUSTED_LOAD_CASE_PERIOD_METHOD

    TIME_PERIOD = 0
    POWER_LOAD_ANGLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InertiaAdjustedLoadCasePeriodMethod.__setattr__ = __enum_setattr
InertiaAdjustedLoadCasePeriodMethod.__delattr__ = __enum_delattr
