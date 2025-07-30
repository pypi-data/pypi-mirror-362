"""FENodeOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_NODE_OPTION = python_net_import("SMT.MastaAPI.NodalAnalysis", "FENodeOption")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FENodeOption")
    CastSelf = TypeVar("CastSelf", bound="FENodeOption._Cast_FENodeOption")


__docformat__ = "restructuredtext en"
__all__ = ("FENodeOption",)


class FENodeOption(Enum):
    """FENodeOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_NODE_OPTION

    NONE = 0
    SURFACE = 1
    ALL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FENodeOption.__setattr__ = __enum_setattr
FENodeOption.__delattr__ = __enum_delattr
