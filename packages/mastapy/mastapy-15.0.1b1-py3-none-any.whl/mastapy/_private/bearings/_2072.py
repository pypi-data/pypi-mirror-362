"""BearingCatalog"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_CATALOG = python_net_import("SMT.MastaAPI.Bearings", "BearingCatalog")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingCatalog")
    CastSelf = TypeVar("CastSelf", bound="BearingCatalog._Cast_BearingCatalog")


__docformat__ = "restructuredtext en"
__all__ = ("BearingCatalog",)


class BearingCatalog(Enum):
    """BearingCatalog

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_CATALOG

    ALL = 0
    TIMKEN = 1
    SKF = 2
    NSK = 3
    INA = 4
    FAG = 5
    JTEKT_KOYO = 6
    NTN = 7
    CUSTOM = 8
    SKF_LEGACY = 9
    SCHAEFFLER_LEGACY = 10
    TIMKEN_LEGACY = 11
    NACHI = 12
    ILJIN = 13
    NES = 14
    JTEKT_KOYO_LEGACY = 15


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingCatalog.__setattr__ = __enum_setattr
BearingCatalog.__delattr__ = __enum_delattr
