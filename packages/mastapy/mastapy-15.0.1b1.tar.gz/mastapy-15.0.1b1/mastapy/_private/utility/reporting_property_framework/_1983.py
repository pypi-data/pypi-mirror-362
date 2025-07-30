"""CellValuePosition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CELL_VALUE_POSITION = python_net_import(
    "SMT.MastaAPI.Utility.ReportingPropertyFramework", "CellValuePosition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CellValuePosition")
    CastSelf = TypeVar("CastSelf", bound="CellValuePosition._Cast_CellValuePosition")


__docformat__ = "restructuredtext en"
__all__ = ("CellValuePosition",)


class CellValuePosition(Enum):
    """CellValuePosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CELL_VALUE_POSITION

    LEFT = 0
    CENTER = 1
    RIGHT = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CellValuePosition.__setattr__ = __enum_setattr
CellValuePosition.__delattr__ = __enum_delattr
