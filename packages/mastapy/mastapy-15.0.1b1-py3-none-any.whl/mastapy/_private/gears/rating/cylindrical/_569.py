"""MisalignmentContactPatternEnhancements"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MISALIGNMENT_CONTACT_PATTERN_ENHANCEMENTS = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical", "MisalignmentContactPatternEnhancements"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MisalignmentContactPatternEnhancements")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MisalignmentContactPatternEnhancements._Cast_MisalignmentContactPatternEnhancements",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MisalignmentContactPatternEnhancements",)


class MisalignmentContactPatternEnhancements(Enum):
    """MisalignmentContactPatternEnhancements

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MISALIGNMENT_CONTACT_PATTERN_ENHANCEMENTS

    CONTACT_PATTERN_UNPROVEN = 0
    CONTACT_PATTERN_FAVOURABLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MisalignmentContactPatternEnhancements.__setattr__ = __enum_setattr
MisalignmentContactPatternEnhancements.__delattr__ = __enum_delattr
