"""AlignmentAxis"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ALIGNMENT_AXIS = python_net_import("SMT.MastaAPI.MathUtility", "AlignmentAxis")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AlignmentAxis")
    CastSelf = TypeVar("CastSelf", bound="AlignmentAxis._Cast_AlignmentAxis")


__docformat__ = "restructuredtext en"
__all__ = ("AlignmentAxis",)


class AlignmentAxis(Enum):
    """AlignmentAxis

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ALIGNMENT_AXIS

    XAXIS_PARALLEL = 0
    XAXIS_ANTIPARALLEL = 1
    YAXIS_PARALLEL = 2
    YAXIS_ANTIPARALLEL = 3
    ZAXIS_PARALLEL = 4
    ZAXIS_ANTIPARALLEL = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AlignmentAxis.__setattr__ = __enum_setattr
AlignmentAxis.__delattr__ = __enum_delattr
