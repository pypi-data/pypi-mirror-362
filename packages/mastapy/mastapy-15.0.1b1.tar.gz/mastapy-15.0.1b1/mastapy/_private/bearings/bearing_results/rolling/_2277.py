"""RollerAnalysisMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROLLER_ANALYSIS_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling", "RollerAnalysisMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerAnalysisMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerAnalysisMethod._Cast_RollerAnalysisMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerAnalysisMethod",)


class RollerAnalysisMethod(Enum):
    """RollerAnalysisMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROLLER_ANALYSIS_METHOD

    THREE_DEGREE_OF_FREEDOM_ROLLERS = 0
    LEGACY_METHOD = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RollerAnalysisMethod.__setattr__ = __enum_setattr
RollerAnalysisMethod.__delattr__ = __enum_delattr
