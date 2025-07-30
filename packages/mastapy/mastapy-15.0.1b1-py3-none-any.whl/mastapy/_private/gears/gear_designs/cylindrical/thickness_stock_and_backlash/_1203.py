"""FinishStockType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FINISH_STOCK_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.ThicknessStockAndBacklash",
    "FinishStockType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FinishStockType")
    CastSelf = TypeVar("CastSelf", bound="FinishStockType._Cast_FinishStockType")


__docformat__ = "restructuredtext en"
__all__ = ("FinishStockType",)


class FinishStockType(Enum):
    """FinishStockType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FINISH_STOCK_TYPE

    NONE = 0
    SINGLE_VALUE = 1
    TOLERANCED_VALUE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FinishStockType.__setattr__ = __enum_setattr
FinishStockType.__delattr__ = __enum_delattr
