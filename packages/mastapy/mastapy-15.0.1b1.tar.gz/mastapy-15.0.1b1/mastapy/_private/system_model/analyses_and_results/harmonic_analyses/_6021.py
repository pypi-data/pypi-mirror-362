"""DampingSpecification"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DAMPING_SPECIFICATION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "DampingSpecification",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DampingSpecification")
    CastSelf = TypeVar(
        "CastSelf", bound="DampingSpecification._Cast_DampingSpecification"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DampingSpecification",)


class DampingSpecification(Enum):
    """DampingSpecification

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DAMPING_SPECIFICATION

    MODAL_DAMPING_FACTORS = 0
    PER_MODE = 1
    PER_FREQUENCY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DampingSpecification.__setattr__ = __enum_setattr
DampingSpecification.__delattr__ = __enum_delattr
