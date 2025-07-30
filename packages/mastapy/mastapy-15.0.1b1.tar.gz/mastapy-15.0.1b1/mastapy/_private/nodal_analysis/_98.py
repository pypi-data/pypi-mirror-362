"""VolumeElementShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_VOLUME_ELEMENT_SHAPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "VolumeElementShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="VolumeElementShape")
    CastSelf = TypeVar("CastSelf", bound="VolumeElementShape._Cast_VolumeElementShape")


__docformat__ = "restructuredtext en"
__all__ = ("VolumeElementShape",)


class VolumeElementShape(Enum):
    """VolumeElementShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _VOLUME_ELEMENT_SHAPE

    TETRAHEDRAL = 0
    HEXAHEDRAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


VolumeElementShape.__setattr__ = __enum_setattr
VolumeElementShape.__delattr__ = __enum_delattr
