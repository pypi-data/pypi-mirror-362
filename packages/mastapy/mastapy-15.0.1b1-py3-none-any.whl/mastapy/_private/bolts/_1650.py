"""AxialLoadType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AXIAL_LOAD_TYPE = python_net_import("SMT.MastaAPI.Bolts", "AxialLoadType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AxialLoadType")
    CastSelf = TypeVar("CastSelf", bound="AxialLoadType._Cast_AxialLoadType")


__docformat__ = "restructuredtext en"
__all__ = ("AxialLoadType",)


class AxialLoadType(Enum):
    """AxialLoadType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AXIAL_LOAD_TYPE

    DYNAMIC_AND_ECCENTRIC = 0
    DYNAMIC_AND_CONCENTRIC = 1
    STATIC_AND_ECCENTRIC = 2
    STATIC_AND_CONCENTRIC = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AxialLoadType.__setattr__ = __enum_setattr
AxialLoadType.__delattr__ = __enum_delattr
