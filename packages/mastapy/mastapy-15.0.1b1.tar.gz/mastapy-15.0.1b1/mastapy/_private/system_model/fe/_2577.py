"""AlignmentMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ALIGNMENT_METHOD = python_net_import("SMT.MastaAPI.SystemModel.FE", "AlignmentMethod")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AlignmentMethod")
    CastSelf = TypeVar("CastSelf", bound="AlignmentMethod._Cast_AlignmentMethod")


__docformat__ = "restructuredtext en"
__all__ = ("AlignmentMethod",)


class AlignmentMethod(Enum):
    """AlignmentMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ALIGNMENT_METHOD

    AUTO = 0
    MANUAL = 1
    DATUM = 2
    REPLACED_SHAFT = 3
    SHAFT = 4
    CONNECTABLE_COMPONENT = 5
    COMPONENT = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AlignmentMethod.__setattr__ = __enum_setattr
AlignmentMethod.__delattr__ = __enum_delattr
