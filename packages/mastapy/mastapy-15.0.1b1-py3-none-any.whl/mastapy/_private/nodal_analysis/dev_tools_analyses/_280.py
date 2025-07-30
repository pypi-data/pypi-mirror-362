"""FESelectionMode"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_SELECTION_MODE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "FESelectionMode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FESelectionMode")
    CastSelf = TypeVar("CastSelf", bound="FESelectionMode._Cast_FESelectionMode")


__docformat__ = "restructuredtext en"
__all__ = ("FESelectionMode",)


class FESelectionMode(Enum):
    """FESelectionMode

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_SELECTION_MODE

    COMPONENT = 0
    NODE_INDIVIDUAL = 1
    NODE_REGION = 2
    SURFACE = 3
    FACE = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FESelectionMode.__setattr__ = __enum_setattr
FESelectionMode.__delattr__ = __enum_delattr
