"""RollerBearingProfileTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROLLER_BEARING_PROFILE_TYPES = python_net_import(
    "SMT.MastaAPI.Bearings", "RollerBearingProfileTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RollerBearingProfileTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="RollerBearingProfileTypes._Cast_RollerBearingProfileTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearingProfileTypes",)


class RollerBearingProfileTypes(Enum):
    """RollerBearingProfileTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROLLER_BEARING_PROFILE_TYPES

    NONE = 0
    LUNDBERG = 1
    DIN_LUNDBERG = 2
    CROWNED = 3
    FUJIWARA_KAWASE = 4
    USERSPECIFIED = 5
    CONICAL = 6
    TANGENTIAL_CROWNED = 7
    JOHNS_GOHAR = 8


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RollerBearingProfileTypes.__setattr__ = __enum_setattr
RollerBearingProfileTypes.__delattr__ = __enum_delattr
