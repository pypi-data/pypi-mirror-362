"""BarModelExportType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BAR_MODEL_EXPORT_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "BarModelExportType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BarModelExportType")
    CastSelf = TypeVar("CastSelf", bound="BarModelExportType._Cast_BarModelExportType")


__docformat__ = "restructuredtext en"
__all__ = ("BarModelExportType",)


class BarModelExportType(Enum):
    """BarModelExportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BAR_MODEL_EXPORT_TYPE

    BAR_ELEMENTS = 0
    MATRIX_ELEMENTS = 1
    SOLID_SHAFTS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BarModelExportType.__setattr__ = __enum_setattr
BarModelExportType.__delattr__ = __enum_delattr
