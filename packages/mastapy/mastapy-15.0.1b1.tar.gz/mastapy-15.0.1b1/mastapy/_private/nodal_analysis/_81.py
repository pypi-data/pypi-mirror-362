"""ModeInputType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MODE_INPUT_TYPE = python_net_import("SMT.MastaAPI.NodalAnalysis", "ModeInputType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ModeInputType")
    CastSelf = TypeVar("CastSelf", bound="ModeInputType._Cast_ModeInputType")


__docformat__ = "restructuredtext en"
__all__ = ("ModeInputType",)


class ModeInputType(Enum):
    """ModeInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MODE_INPUT_TYPE

    NO_MODES = 0
    ALL_IN_RANGE = 1
    LOWEST_IN_RANGE = 2
    NEAREST_TO_SHIFT = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ModeInputType.__setattr__ = __enum_setattr
ModeInputType.__delattr__ = __enum_delattr
