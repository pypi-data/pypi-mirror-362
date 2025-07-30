"""NodeSelectionDepthOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_NODE_SELECTION_DEPTH_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.FE", "NodeSelectionDepthOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="NodeSelectionDepthOption")
    CastSelf = TypeVar(
        "CastSelf", bound="NodeSelectionDepthOption._Cast_NodeSelectionDepthOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("NodeSelectionDepthOption",)


class NodeSelectionDepthOption(Enum):
    """NodeSelectionDepthOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _NODE_SELECTION_DEPTH_OPTION

    SURFACE_NODES = 0
    SOLID_NODES = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


NodeSelectionDepthOption.__setattr__ = __enum_setattr
NodeSelectionDepthOption.__delattr__ = __enum_delattr
