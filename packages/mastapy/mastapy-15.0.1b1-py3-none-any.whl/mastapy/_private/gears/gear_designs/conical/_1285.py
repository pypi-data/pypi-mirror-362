"""GleasonSafetyRequirements"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GLEASON_SAFETY_REQUIREMENTS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "GleasonSafetyRequirements"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GleasonSafetyRequirements")
    CastSelf = TypeVar(
        "CastSelf", bound="GleasonSafetyRequirements._Cast_GleasonSafetyRequirements"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GleasonSafetyRequirements",)


class GleasonSafetyRequirements(Enum):
    """GleasonSafetyRequirements

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GLEASON_SAFETY_REQUIREMENTS

    MAXIMUM_SAFETY = 0
    FEWER_THAN_1_FAILURE_IN_100 = 1
    FEWER_THAN_1_FAILURE_IN_3 = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GleasonSafetyRequirements.__setattr__ = __enum_setattr
GleasonSafetyRequirements.__delattr__ = __enum_delattr
