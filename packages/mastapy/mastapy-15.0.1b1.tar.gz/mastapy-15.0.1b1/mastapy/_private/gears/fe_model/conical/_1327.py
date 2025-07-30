"""FlankDataSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FLANK_DATA_SOURCE = python_net_import(
    "SMT.MastaAPI.Gears.FEModel.Conical", "FlankDataSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FlankDataSource")
    CastSelf = TypeVar("CastSelf", bound="FlankDataSource._Cast_FlankDataSource")


__docformat__ = "restructuredtext en"
__all__ = ("FlankDataSource",)


class FlankDataSource(Enum):
    """FlankDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FLANK_DATA_SOURCE

    MACRODESIGN = 0
    MANUFACTURING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FlankDataSource.__setattr__ = __enum_setattr
FlankDataSource.__delattr__ = __enum_delattr
