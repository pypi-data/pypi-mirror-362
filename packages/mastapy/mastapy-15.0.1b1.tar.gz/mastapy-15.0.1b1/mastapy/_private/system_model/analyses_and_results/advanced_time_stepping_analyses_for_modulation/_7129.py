"""AtsamExcitationsOrOthers"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ATSAM_EXCITATIONS_OR_OTHERS = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedTimeSteppingAnalysesForModulation",
    "AtsamExcitationsOrOthers",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AtsamExcitationsOrOthers")
    CastSelf = TypeVar(
        "CastSelf", bound="AtsamExcitationsOrOthers._Cast_AtsamExcitationsOrOthers"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AtsamExcitationsOrOthers",)


class AtsamExcitationsOrOthers(Enum):
    """AtsamExcitationsOrOthers

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ATSAM_EXCITATIONS_OR_OTHERS

    ADVANCED_MODEL = 0
    OTHER_EXCITATIONS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AtsamExcitationsOrOthers.__setattr__ = __enum_setattr
AtsamExcitationsOrOthers.__delattr__ = __enum_delattr
