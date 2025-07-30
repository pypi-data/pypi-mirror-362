"""ElementOrder"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELEMENT_ORDER = python_net_import("SMT.MastaAPI.NodalAnalysis", "ElementOrder")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementOrder")
    CastSelf = TypeVar("CastSelf", bound="ElementOrder._Cast_ElementOrder")


__docformat__ = "restructuredtext en"
__all__ = ("ElementOrder",)


class ElementOrder(Enum):
    """ElementOrder

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELEMENT_ORDER

    LINEAR = 0
    QUADRATIC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElementOrder.__setattr__ = __enum_setattr
ElementOrder.__delattr__ = __enum_delattr
