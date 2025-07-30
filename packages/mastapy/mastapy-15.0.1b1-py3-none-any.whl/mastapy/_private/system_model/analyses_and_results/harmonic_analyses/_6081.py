"""ModalCorrectionMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MODAL_CORRECTION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "ModalCorrectionMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModalCorrectionMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="ModalCorrectionMethod._Cast_ModalCorrectionMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModalCorrectionMethod",)


class ModalCorrectionMethod(Enum):
    """ModalCorrectionMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MODAL_CORRECTION_METHOD

    NONE = 0
    INCLUDE_RESIDUAL_VECTORS = 1
    INCLUDE_TRUNCATION_CORRECTION = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ModalCorrectionMethod.__setattr__ = __enum_setattr
ModalCorrectionMethod.__delattr__ = __enum_delattr
