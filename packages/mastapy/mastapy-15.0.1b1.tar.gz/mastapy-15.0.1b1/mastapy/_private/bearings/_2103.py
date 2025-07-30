"""TiltingPadTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TILTING_PAD_TYPES = python_net_import("SMT.MastaAPI.Bearings", "TiltingPadTypes")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TiltingPadTypes")
    CastSelf = TypeVar("CastSelf", bound="TiltingPadTypes._Cast_TiltingPadTypes")


__docformat__ = "restructuredtext en"
__all__ = ("TiltingPadTypes",)


class TiltingPadTypes(Enum):
    """TiltingPadTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TILTING_PAD_TYPES

    NONEQUALISED = 0
    EQUALISED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TiltingPadTypes.__setattr__ = __enum_setattr
TiltingPadTypes.__delattr__ = __enum_delattr
