"""CadPageOrientation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CAD_PAGE_ORIENTATION = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CadPageOrientation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CadPageOrientation")
    CastSelf = TypeVar("CastSelf", bound="CadPageOrientation._Cast_CadPageOrientation")


__docformat__ = "restructuredtext en"
__all__ = ("CadPageOrientation",)


class CadPageOrientation(Enum):
    """CadPageOrientation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CAD_PAGE_ORIENTATION

    LANDSCAPE = 0
    PORTRAIT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CadPageOrientation.__setattr__ = __enum_setattr
CadPageOrientation.__delattr__ = __enum_delattr
