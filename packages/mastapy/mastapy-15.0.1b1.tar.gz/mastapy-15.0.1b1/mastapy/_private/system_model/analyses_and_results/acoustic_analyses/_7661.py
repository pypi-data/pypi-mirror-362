"""AcousticAnalysisRunType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACOUSTIC_ANALYSIS_RUN_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "AcousticAnalysisRunType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticAnalysisRunType")
    CastSelf = TypeVar(
        "CastSelf", bound="AcousticAnalysisRunType._Cast_AcousticAnalysisRunType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticAnalysisRunType",)


class AcousticAnalysisRunType(Enum):
    """AcousticAnalysisRunType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACOUSTIC_ANALYSIS_RUN_TYPE

    BY_EXCITATION = 0
    BY_ORDER = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AcousticAnalysisRunType.__setattr__ = __enum_setattr
AcousticAnalysisRunType.__delattr__ = __enum_delattr
