"""BearingNodeOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_NODE_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "BearingNodeOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingNodeOption")
    CastSelf = TypeVar("CastSelf", bound="BearingNodeOption._Cast_BearingNodeOption")


__docformat__ = "restructuredtext en"
__all__ = ("BearingNodeOption",)


class BearingNodeOption(Enum):
    """BearingNodeOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_NODE_OPTION

    SINGLE_NODE_FOR_BEARING = 0
    NODE_PER_BEARING_ROW = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingNodeOption.__setattr__ = __enum_setattr
BearingNodeOption.__delattr__ = __enum_delattr
