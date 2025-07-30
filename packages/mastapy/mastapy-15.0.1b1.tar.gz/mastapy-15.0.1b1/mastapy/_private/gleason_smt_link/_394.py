"""CutterMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CUTTER_METHOD = python_net_import("SMT.MastaAPI.GleasonSMTLink", "CutterMethod")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CutterMethod")
    CastSelf = TypeVar("CastSelf", bound="CutterMethod._Cast_CutterMethod")


__docformat__ = "restructuredtext en"
__all__ = ("CutterMethod",)


class CutterMethod(Enum):
    """CutterMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CUTTER_METHOD

    FACE_MILLING = 1
    FACE_HOBBING = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CutterMethod.__setattr__ = __enum_setattr
CutterMethod.__delattr__ = __enum_delattr
