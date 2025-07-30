"""LoadingStatus"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOADING_STATUS = python_net_import("SMT.MastaAPI.NodalAnalysis", "LoadingStatus")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadingStatus")
    CastSelf = TypeVar("CastSelf", bound="LoadingStatus._Cast_LoadingStatus")


__docformat__ = "restructuredtext en"
__all__ = ("LoadingStatus",)


class LoadingStatus(Enum):
    """LoadingStatus

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOADING_STATUS

    UNLOADED = 0
    LOADED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadingStatus.__setattr__ = __enum_setattr
LoadingStatus.__delattr__ = __enum_delattr
