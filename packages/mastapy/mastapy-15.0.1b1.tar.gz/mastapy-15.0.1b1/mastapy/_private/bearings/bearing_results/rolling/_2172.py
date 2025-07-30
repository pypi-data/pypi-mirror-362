"""BallBearingAnalysisMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BALL_BEARING_ANALYSIS_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "BallBearingAnalysisMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BallBearingAnalysisMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="BallBearingAnalysisMethod._Cast_BallBearingAnalysisMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BallBearingAnalysisMethod",)


class BallBearingAnalysisMethod(Enum):
    """BallBearingAnalysisMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BALL_BEARING_ANALYSIS_METHOD

    TWO_DEGREES_OF_FREEDOM = 0
    TWO_DEGREES_OF_FREEDOM_IN_SIX_DOF_FRAMEWORK = 1
    SIX_DEGREES_OF_FREEDOM_COULOMB = 2
    SIX_DEGREES_OF_FREEDOM_ADVANCED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BallBearingAnalysisMethod.__setattr__ = __enum_setattr
BallBearingAnalysisMethod.__delattr__ = __enum_delattr
