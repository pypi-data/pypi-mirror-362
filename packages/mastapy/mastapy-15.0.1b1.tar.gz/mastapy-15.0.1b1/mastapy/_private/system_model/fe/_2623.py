"""LinkNodeSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LINK_NODE_SOURCE = python_net_import("SMT.MastaAPI.SystemModel.FE", "LinkNodeSource")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LinkNodeSource")
    CastSelf = TypeVar("CastSelf", bound="LinkNodeSource._Cast_LinkNodeSource")


__docformat__ = "restructuredtext en"
__all__ = ("LinkNodeSource",)


class LinkNodeSource(Enum):
    """LinkNodeSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LINK_NODE_SOURCE

    EXISTING_CONDENSATION_NODE = 0
    CREATE_SINGLE_AXIAL_NODE = 1
    CREATE_NODES_AT_ANGLES = 2
    CREATE_FLEXIBLE_NODE_RING = 3
    NONE = 4
    USE_NODES_FROM_ANOTHER_LINK = 5
    CREATE_ONE_NODE_PER_TOOTH = 6
    FLANK_NODES = 7


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LinkNodeSource.__setattr__ = __enum_setattr
LinkNodeSource.__delattr__ = __enum_delattr
