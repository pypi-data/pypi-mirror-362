"""CandidateDisplayChoice"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CANDIDATE_DISPLAY_CHOICE = python_net_import(
    "SMT.MastaAPI.Gears.GearSetParetoOptimiser", "CandidateDisplayChoice"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CandidateDisplayChoice")
    CastSelf = TypeVar(
        "CastSelf", bound="CandidateDisplayChoice._Cast_CandidateDisplayChoice"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CandidateDisplayChoice",)


class CandidateDisplayChoice(Enum):
    """CandidateDisplayChoice

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CANDIDATE_DISPLAY_CHOICE

    ALL_FEASIBLE_CANDIDATES = 0
    CANDIDATES_AFTER_FILTERING = 1
    DOMINANT_CANDIDATES = 2
    CANDIDATES_SELECTED_IN_CHART = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CandidateDisplayChoice.__setattr__ = __enum_setattr
CandidateDisplayChoice.__delattr__ = __enum_delattr
