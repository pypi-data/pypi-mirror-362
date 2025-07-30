"""FEMeshingOperation"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_MESHING_OPERATION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "FEMeshingOperation"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEMeshingOperation")
    CastSelf = TypeVar("CastSelf", bound="FEMeshingOperation._Cast_FEMeshingOperation")


__docformat__ = "restructuredtext en"
__all__ = ("FEMeshingOperation",)


class FEMeshingOperation(Enum):
    """FEMeshingOperation

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_MESHING_OPERATION

    SURFACE = 0
    VOLUME = 1
    CROSS_SECTION = 2
    CROSS_SECTION_TRIANGULATION = 3
    CROSS_SECTION_BOUNDARY = 4
    SURFACE_MESH_INPUT = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FEMeshingOperation.__setattr__ = __enum_setattr
FEMeshingOperation.__delattr__ = __enum_delattr
