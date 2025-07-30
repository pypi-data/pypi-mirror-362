"""LoadedBallElementPropertyType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOADED_BALL_ELEMENT_PROPERTY_TYPE = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBallElementPropertyType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadedBallElementPropertyType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LoadedBallElementPropertyType._Cast_LoadedBallElementPropertyType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBallElementPropertyType",)


class LoadedBallElementPropertyType(Enum):
    """LoadedBallElementPropertyType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOADED_BALL_ELEMENT_PROPERTY_TYPE

    ELEMENT_WITH_HIGHEST_SLIDING_SPEED = 0
    ELEMENT_WITH_HIGHEST_PRESSURE_VELOCITY = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadedBallElementPropertyType.__setattr__ = __enum_setattr
LoadedBallElementPropertyType.__delattr__ = __enum_delattr
