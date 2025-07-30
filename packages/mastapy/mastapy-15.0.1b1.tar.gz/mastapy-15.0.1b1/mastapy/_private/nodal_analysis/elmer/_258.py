"""NodalAverageType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NODAL_AVERAGE_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.Elmer", "NodalAverageType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NodalAverageType")
    CastSelf = TypeVar("CastSelf", bound="NodalAverageType._Cast_NodalAverageType")


__docformat__ = "restructuredtext en"
__all__ = ("NodalAverageType",)


class NodalAverageType(Enum):
    """NodalAverageType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NODAL_AVERAGE_TYPE

    UNIFORM = 0
    GEOMETRIC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NodalAverageType.__setattr__ = __enum_setattr
NodalAverageType.__delattr__ = __enum_delattr
