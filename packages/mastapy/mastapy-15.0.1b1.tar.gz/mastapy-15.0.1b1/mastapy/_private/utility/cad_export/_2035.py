"""DxfVersionWithName"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DXF_VERSION_WITH_NAME = python_net_import(
    "SMT.MastaAPI.Utility.CadExport", "DxfVersionWithName"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DxfVersionWithName")
    CastSelf = TypeVar("CastSelf", bound="DxfVersionWithName._Cast_DxfVersionWithName")


__docformat__ = "restructuredtext en"
__all__ = ("DxfVersionWithName",)


class DxfVersionWithName(Enum):
    """DxfVersionWithName

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DXF_VERSION_WITH_NAME

    REVISION_13101_AUTOCAD_RELEASE_13_AC1012 = 12
    REVISION_14104_AUTOCAD_RELEASE_14_AC1014 = 14
    REVISION_15002_AUTOCAD_2000_2002_AC1015 = 15
    REVISION_18101_AUTOCAD_2004_AC1018 = 18
    REVISION_21101_AUTOCAD_2007_AC1021 = 21
    REVISION_24101_AUTOCAD_2010_AC1024 = 24
    REVISION_27_AUTOCAD_2013_AC1027 = 27


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DxfVersionWithName.__setattr__ = __enum_setattr
DxfVersionWithName.__delattr__ = __enum_delattr
