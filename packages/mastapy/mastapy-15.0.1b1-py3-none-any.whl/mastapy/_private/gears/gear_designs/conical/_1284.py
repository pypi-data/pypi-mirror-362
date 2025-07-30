"""FrontEndTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FRONT_END_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "FrontEndTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FrontEndTypes")
    CastSelf = TypeVar("CastSelf", bound="FrontEndTypes._Cast_FrontEndTypes")


__docformat__ = "restructuredtext en"
__all__ = ("FrontEndTypes",)


class FrontEndTypes(Enum):
    """FrontEndTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FRONT_END_TYPES

    FLAT = 0
    CONICAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FrontEndTypes.__setattr__ = __enum_setattr
FrontEndTypes.__delattr__ = __enum_delattr
