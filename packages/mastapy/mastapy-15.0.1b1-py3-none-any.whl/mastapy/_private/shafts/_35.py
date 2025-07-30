"""ShaftProfileType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHAFT_PROFILE_TYPE = python_net_import("SMT.MastaAPI.Shafts", "ShaftProfileType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftProfileType")
    CastSelf = TypeVar("CastSelf", bound="ShaftProfileType._Cast_ShaftProfileType")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftProfileType",)


class ShaftProfileType(Enum):
    """ShaftProfileType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHAFT_PROFILE_TYPE

    WITHOUT_FEATURES = 0
    WITH_FEATURES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShaftProfileType.__setattr__ = __enum_setattr
ShaftProfileType.__delattr__ = __enum_delattr
