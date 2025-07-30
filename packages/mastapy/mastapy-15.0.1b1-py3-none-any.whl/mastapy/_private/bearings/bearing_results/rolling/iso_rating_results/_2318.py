"""StressConcentrationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STRESS_CONCENTRATION_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.IsoRatingResults",
    "StressConcentrationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StressConcentrationMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="StressConcentrationMethod._Cast_StressConcentrationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StressConcentrationMethod",)


class StressConcentrationMethod(Enum):
    """StressConcentrationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STRESS_CONCENTRATION_METHOD

    BASIC_STRESS_RISER_FUNCTION = 0
    CALCULATED_STRESSES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StressConcentrationMethod.__setattr__ = __enum_setattr
StressConcentrationMethod.__delattr__ = __enum_delattr
