"""FEMeshElementEntityOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_MESH_ELEMENT_ENTITY_OPTION = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "FEMeshElementEntityOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEMeshElementEntityOption")
    CastSelf = TypeVar(
        "CastSelf", bound="FEMeshElementEntityOption._Cast_FEMeshElementEntityOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("FEMeshElementEntityOption",)


class FEMeshElementEntityOption(Enum):
    """FEMeshElementEntityOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_MESH_ELEMENT_ENTITY_OPTION

    NONE = 0
    ALL = 1
    FREE_FACES = 2
    OUTLINE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FEMeshElementEntityOption.__setattr__ = __enum_setattr
FEMeshElementEntityOption.__delattr__ = __enum_delattr
