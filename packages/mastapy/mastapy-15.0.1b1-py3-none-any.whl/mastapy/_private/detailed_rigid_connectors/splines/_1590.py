"""RootTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ROOT_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "RootTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RootTypes")
    CastSelf = TypeVar("CastSelf", bound="RootTypes._Cast_RootTypes")


__docformat__ = "restructuredtext en"
__all__ = ("RootTypes",)


class RootTypes(Enum):
    """RootTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ROOT_TYPES

    FLAT_ROOT = 0
    FILLET_ROOT = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RootTypes.__setattr__ = __enum_setattr
RootTypes.__delattr__ = __enum_delattr
