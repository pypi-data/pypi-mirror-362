"""AGMALoadSharingTableApplicationLevel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AGMA_LOAD_SHARING_TABLE_APPLICATION_LEVEL = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "AGMALoadSharingTableApplicationLevel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMALoadSharingTableApplicationLevel")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AGMALoadSharingTableApplicationLevel._Cast_AGMALoadSharingTableApplicationLevel",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AGMALoadSharingTableApplicationLevel",)


class AGMALoadSharingTableApplicationLevel(Enum):
    """AGMALoadSharingTableApplicationLevel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AGMA_LOAD_SHARING_TABLE_APPLICATION_LEVEL

    APPLICATION_LEVEL_1 = 0
    APPLICATION_LEVEL_2 = 1
    APPLICATION_LEVEL_3 = 2
    APPLICATION_LEVEL_4 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AGMALoadSharingTableApplicationLevel.__setattr__ = __enum_setattr
AGMALoadSharingTableApplicationLevel.__delattr__ = __enum_delattr
