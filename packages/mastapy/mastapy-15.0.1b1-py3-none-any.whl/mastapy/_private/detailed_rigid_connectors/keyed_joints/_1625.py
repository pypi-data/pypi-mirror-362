"""NumberOfKeys"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NUMBER_OF_KEYS = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.KeyedJoints", "NumberOfKeys"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NumberOfKeys")
    CastSelf = TypeVar("CastSelf", bound="NumberOfKeys._Cast_NumberOfKeys")


__docformat__ = "restructuredtext en"
__all__ = ("NumberOfKeys",)


class NumberOfKeys(Enum):
    """NumberOfKeys

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NUMBER_OF_KEYS

    _1 = 0
    _2 = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NumberOfKeys.__setattr__ = __enum_setattr
NumberOfKeys.__delattr__ = __enum_delattr
