"""DegreeOfFreedomType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DEGREE_OF_FREEDOM_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses.FullFEReporting", "DegreeOfFreedomType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DegreeOfFreedomType")
    CastSelf = TypeVar(
        "CastSelf", bound="DegreeOfFreedomType._Cast_DegreeOfFreedomType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DegreeOfFreedomType",)


class DegreeOfFreedomType(Enum):
    """DegreeOfFreedomType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DEGREE_OF_FREEDOM_TYPE

    INDEPENDENT = 0
    DEPENDENT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DegreeOfFreedomType.__setattr__ = __enum_setattr
DegreeOfFreedomType.__delattr__ = __enum_delattr
