"""MotoringOrGenerating"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MOTORING_OR_GENERATING = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "MotoringOrGenerating"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MotoringOrGenerating")
    CastSelf = TypeVar(
        "CastSelf", bound="MotoringOrGenerating._Cast_MotoringOrGenerating"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MotoringOrGenerating",)


class MotoringOrGenerating(Enum):
    """MotoringOrGenerating

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MOTORING_OR_GENERATING

    MOTORING = 0
    GENERATING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MotoringOrGenerating.__setattr__ = __enum_setattr
MotoringOrGenerating.__delattr__ = __enum_delattr
