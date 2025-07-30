"""ModalContributionDisplayMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MODAL_CONTRIBUTION_DISPLAY_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.Results",
    "ModalContributionDisplayMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModalContributionDisplayMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ModalContributionDisplayMethod._Cast_ModalContributionDisplayMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalContributionDisplayMethod",)


class ModalContributionDisplayMethod(Enum):
    """ModalContributionDisplayMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MODAL_CONTRIBUTION_DISPLAY_METHOD

    ALL_MODES = 0
    MODE_INDEX = 1
    MODE_INDEX_RANGE = 2
    MODE_FREQUENCY_RANGE = 3
    MODAL_CORRECTIONS = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ModalContributionDisplayMethod.__setattr__ = __enum_setattr
ModalContributionDisplayMethod.__delattr__ = __enum_delattr
