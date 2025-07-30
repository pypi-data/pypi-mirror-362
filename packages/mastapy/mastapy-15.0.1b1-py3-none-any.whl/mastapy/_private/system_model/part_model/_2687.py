"""LoadSharingModes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOAD_SHARING_MODES = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "LoadSharingModes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadSharingModes")
    CastSelf = TypeVar("CastSelf", bound="LoadSharingModes._Cast_LoadSharingModes")


__docformat__ = "restructuredtext en"
__all__ = ("LoadSharingModes",)


class LoadSharingModes(Enum):
    """LoadSharingModes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOAD_SHARING_MODES

    EQUAL = 0
    USERDEFINED = 1
    AGMA_EMPIRICAL = 2
    GL = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadSharingModes.__setattr__ = __enum_setattr
LoadSharingModes.__delattr__ = __enum_delattr
