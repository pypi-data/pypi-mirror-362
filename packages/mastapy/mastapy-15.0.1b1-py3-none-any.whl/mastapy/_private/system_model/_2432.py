"""RelativeOffsetOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RELATIVE_OFFSET_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel", "RelativeOffsetOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RelativeOffsetOption")
    CastSelf = TypeVar(
        "CastSelf", bound="RelativeOffsetOption._Cast_RelativeOffsetOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RelativeOffsetOption",)


class RelativeOffsetOption(Enum):
    """RelativeOffsetOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RELATIVE_OFFSET_OPTION

    LEFT = 0
    CENTRE = 1
    RIGHT = 2
    SPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RelativeOffsetOption.__setattr__ = __enum_setattr
RelativeOffsetOption.__delattr__ = __enum_delattr
