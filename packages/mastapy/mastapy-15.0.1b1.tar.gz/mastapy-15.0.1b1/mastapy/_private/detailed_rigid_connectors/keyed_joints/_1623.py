"""KeyTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_KEY_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints", "KeyTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="KeyTypes")
    CastSelf = TypeVar("CastSelf", bound="KeyTypes._Cast_KeyTypes")


__docformat__ = "restructuredtext en"
__all__ = ("KeyTypes",)


class KeyTypes(Enum):
    """KeyTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _KEY_TYPES

    TYPE_A = 0
    TYPE_B = 1
    TYPE_AB = 2
    TYPE_C = 3
    TYPE_D = 4
    TYPE_E = 5
    TYPE_F = 6
    TYPE_G = 7
    TYPE_H = 8
    TYPE_J = 9


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


KeyTypes.__setattr__ = __enum_setattr
KeyTypes.__delattr__ = __enum_delattr
