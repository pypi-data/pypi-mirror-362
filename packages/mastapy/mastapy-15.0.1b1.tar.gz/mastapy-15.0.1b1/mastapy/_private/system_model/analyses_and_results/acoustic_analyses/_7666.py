"""InitialGuessOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INITIAL_GUESS_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses", "InitialGuessOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="InitialGuessOption")
    CastSelf = TypeVar("CastSelf", bound="InitialGuessOption._Cast_InitialGuessOption")


__docformat__ = "restructuredtext en"
__all__ = ("InitialGuessOption",)


class InitialGuessOption(Enum):
    """InitialGuessOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INITIAL_GUESS_OPTION

    ZERO = 0
    EQUIVALENT_RADIATED_POWER_ERP = 1
    RIGHT_HAND_SIDE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


InitialGuessOption.__setattr__ = __enum_setattr
InitialGuessOption.__delattr__ = __enum_delattr
