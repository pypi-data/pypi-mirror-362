"""FEMeshingProblems"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_MESHING_PROBLEMS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "FEMeshingProblems"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEMeshingProblems")
    CastSelf = TypeVar("CastSelf", bound="FEMeshingProblems._Cast_FEMeshingProblems")


__docformat__ = "restructuredtext en"
__all__ = ("FEMeshingProblems",)


class FEMeshingProblems(Enum):
    """FEMeshingProblems

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_MESHING_PROBLEMS

    FREE_EDGE_TRIANGLES = 0
    INTERSECTING_TRIANGLES = 1
    NONMANIFOLD_TRIANGLES = 2
    INCONSISTENT_TRIANGLES = 3
    PENETRATING_TRIANGLES = 4
    UNRECOVERED_EDGES = 5
    UNRECOVERED_FACES = 6
    UNPURGED_POINTS = 7
    UNCONNECTED_POINTS = 8
    ZERO_ANGLE_FACES = 9
    NOT_INSERTED_NODES = 10
    NODES_OUTSIDE_DOMAIN = 11
    FREE_END_LINES = 12
    INCONSISTENT_LINES = 13
    INTERSECTING_LINES = 14
    NONMANIFOLD_LINES = 15


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FEMeshingProblems.__setattr__ = __enum_setattr
FEMeshingProblems.__delattr__ = __enum_delattr
