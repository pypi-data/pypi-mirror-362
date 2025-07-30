"""StrengthGrades"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STRENGTH_GRADES = python_net_import("SMT.MastaAPI.Bolts", "StrengthGrades")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StrengthGrades")
    CastSelf = TypeVar("CastSelf", bound="StrengthGrades._Cast_StrengthGrades")


__docformat__ = "restructuredtext en"
__all__ = ("StrengthGrades",)


class StrengthGrades(Enum):
    """StrengthGrades

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STRENGTH_GRADES

    _129 = 0
    _109 = 1
    _88 = 2
    OTHER = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StrengthGrades.__setattr__ = __enum_setattr
StrengthGrades.__delattr__ = __enum_delattr
