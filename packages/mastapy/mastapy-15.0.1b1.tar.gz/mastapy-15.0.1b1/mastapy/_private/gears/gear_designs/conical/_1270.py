"""ActiveConicalFlank"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACTIVE_CONICAL_FLANK = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ActiveConicalFlank"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ActiveConicalFlank")
    CastSelf = TypeVar("CastSelf", bound="ActiveConicalFlank._Cast_ActiveConicalFlank")


__docformat__ = "restructuredtext en"
__all__ = ("ActiveConicalFlank",)


class ActiveConicalFlank(Enum):
    """ActiveConicalFlank

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACTIVE_CONICAL_FLANK

    DRIVE = 0
    COAST = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ActiveConicalFlank.__setattr__ = __enum_setattr
ActiveConicalFlank.__delattr__ = __enum_delattr
