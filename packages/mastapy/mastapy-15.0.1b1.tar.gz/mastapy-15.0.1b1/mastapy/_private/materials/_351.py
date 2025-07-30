"""LubricantDelivery"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LUBRICANT_DELIVERY = python_net_import("SMT.MastaAPI.Materials", "LubricantDelivery")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LubricantDelivery")
    CastSelf = TypeVar("CastSelf", bound="LubricantDelivery._Cast_LubricantDelivery")


__docformat__ = "restructuredtext en"
__all__ = ("LubricantDelivery",)


class LubricantDelivery(Enum):
    """LubricantDelivery

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LUBRICANT_DELIVERY

    SEALED = 0
    SPLASH = 1
    FEED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LubricantDelivery.__setattr__ = __enum_setattr
LubricantDelivery.__delattr__ = __enum_delattr
