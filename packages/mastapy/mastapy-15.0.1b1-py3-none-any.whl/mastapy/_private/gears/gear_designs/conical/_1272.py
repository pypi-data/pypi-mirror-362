"""ConicalFlanks"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONICAL_FLANKS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalFlanks"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalFlanks")
    CastSelf = TypeVar("CastSelf", bound="ConicalFlanks._Cast_ConicalFlanks")


__docformat__ = "restructuredtext en"
__all__ = ("ConicalFlanks",)


class ConicalFlanks(Enum):
    """ConicalFlanks

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONICAL_FLANKS

    CONCAVE = 0
    CONVEX = 1
    WORST = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConicalFlanks.__setattr__ = __enum_setattr
ConicalFlanks.__delattr__ = __enum_delattr
