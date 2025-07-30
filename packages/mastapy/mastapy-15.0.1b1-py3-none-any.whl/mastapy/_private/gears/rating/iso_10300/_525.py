"""MountingConditionsOfPinionAndWheel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MOUNTING_CONDITIONS_OF_PINION_AND_WHEEL = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Iso10300", "MountingConditionsOfPinionAndWheel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MountingConditionsOfPinionAndWheel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="MountingConditionsOfPinionAndWheel._Cast_MountingConditionsOfPinionAndWheel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("MountingConditionsOfPinionAndWheel",)


class MountingConditionsOfPinionAndWheel(Enum):
    """MountingConditionsOfPinionAndWheel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MOUNTING_CONDITIONS_OF_PINION_AND_WHEEL

    NEITHER_MEMBER_CANTILEVER_MOUNTED = 0
    ONE_MEMBER_CANTILEVER_MOUNTED = 1
    BOTH_MEMBER_CANTILEVER_MOUNTED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MountingConditionsOfPinionAndWheel.__setattr__ = __enum_setattr
MountingConditionsOfPinionAndWheel.__delattr__ = __enum_delattr
