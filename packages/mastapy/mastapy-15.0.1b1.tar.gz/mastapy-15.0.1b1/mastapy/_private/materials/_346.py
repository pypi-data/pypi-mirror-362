"""GreaseContaminationOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GREASE_CONTAMINATION_OPTIONS = python_net_import(
    "SMT.MastaAPI.Materials", "GreaseContaminationOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GreaseContaminationOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="GreaseContaminationOptions._Cast_GreaseContaminationOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GreaseContaminationOptions",)


class GreaseContaminationOptions(Enum):
    """GreaseContaminationOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GREASE_CONTAMINATION_OPTIONS

    HIGH_CLEANLINESS = 0
    NORMAL_CLEANLINESS = 1
    SLIGHTTYPICAL_CONTAMINATION = 2
    SEVERE_CONTAMINATION = 3
    VERY_SEVERE_CONTAMINATION = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GreaseContaminationOptions.__setattr__ = __enum_setattr
GreaseContaminationOptions.__delattr__ = __enum_delattr
