"""CadTableBorderType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CAD_TABLE_BORDER_TYPE = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CadTableBorderType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CadTableBorderType")
    CastSelf = TypeVar("CastSelf", bound="CadTableBorderType._Cast_CadTableBorderType")


__docformat__ = "restructuredtext en"
__all__ = ("CadTableBorderType",)


class CadTableBorderType(Enum):
    """CadTableBorderType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CAD_TABLE_BORDER_TYPE

    SINGLE = 0
    DOUBLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CadTableBorderType.__setattr__ = __enum_setattr
CadTableBorderType.__delattr__ = __enum_delattr
