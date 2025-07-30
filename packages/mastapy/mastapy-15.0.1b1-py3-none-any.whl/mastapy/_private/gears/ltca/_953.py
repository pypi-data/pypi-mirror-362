"""UseAdvancedLTCAOptions"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_USE_ADVANCED_LTCA_OPTIONS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "UseAdvancedLTCAOptions"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UseAdvancedLTCAOptions")
    CastSelf = TypeVar(
        "CastSelf", bound="UseAdvancedLTCAOptions._Cast_UseAdvancedLTCAOptions"
    )


__docformat__ = "restructuredtext en"
__all__ = ("UseAdvancedLTCAOptions",)


class UseAdvancedLTCAOptions(Enum):
    """UseAdvancedLTCAOptions

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _USE_ADVANCED_LTCA_OPTIONS

    YES = 0
    NO = 1
    SPECIFY_FOR_EACH_MESH = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


UseAdvancedLTCAOptions.__setattr__ = __enum_setattr
UseAdvancedLTCAOptions.__delattr__ = __enum_delattr
