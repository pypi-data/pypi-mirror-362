"""OctreeCreationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OCTREE_CREATION_METHOD = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AcousticAnalyses",
    "OctreeCreationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OctreeCreationMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="OctreeCreationMethod._Cast_OctreeCreationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OctreeCreationMethod",)


class OctreeCreationMethod(Enum):
    """OctreeCreationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OCTREE_CREATION_METHOD

    ADAPTIVE = 0
    FIXED_LEVEL = 1
    BENCHMARK = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OctreeCreationMethod.__setattr__ = __enum_setattr
OctreeCreationMethod.__delattr__ = __enum_delattr
