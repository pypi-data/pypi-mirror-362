"""ContactType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONTACT_TYPE = python_net_import("SMT.MastaAPI.NodalAnalysis.Elmer", "ContactType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactType")
    CastSelf = TypeVar("CastSelf", bound="ContactType._Cast_ContactType")


__docformat__ = "restructuredtext en"
__all__ = ("ContactType",)


class ContactType(Enum):
    """ContactType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONTACT_TYPE

    NONE = 0
    TIED = 1
    FRICTION = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ContactType.__setattr__ = __enum_setattr
ContactType.__delattr__ = __enum_delattr
