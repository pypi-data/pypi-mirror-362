"""BearingNodeAlignmentOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_NODE_ALIGNMENT_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "BearingNodeAlignmentOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingNodeAlignmentOption")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingNodeAlignmentOption._Cast_BearingNodeAlignmentOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingNodeAlignmentOption",)


class BearingNodeAlignmentOption(Enum):
    """BearingNodeAlignmentOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_NODE_ALIGNMENT_OPTION

    CENTRE_OF_BEARING = 0
    CENTRE_OF_RACE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingNodeAlignmentOption.__setattr__ = __enum_setattr
BearingNodeAlignmentOption.__delattr__ = __enum_delattr
