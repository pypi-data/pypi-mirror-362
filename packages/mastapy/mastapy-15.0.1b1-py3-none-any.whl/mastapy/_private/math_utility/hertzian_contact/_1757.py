"""ContactDampingModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONTACT_DAMPING_MODEL = python_net_import(
    "SMT.MastaAPI.MathUtility.HertzianContact", "ContactDampingModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactDampingModel")
    CastSelf = TypeVar(
        "CastSelf", bound="ContactDampingModel._Cast_ContactDampingModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactDampingModel",)


class ContactDampingModel(Enum):
    """ContactDampingModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONTACT_DAMPING_MODEL

    RAYLEIGH = 0
    CONSTANT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ContactDampingModel.__setattr__ = __enum_setattr
ContactDampingModel.__delattr__ = __enum_delattr
