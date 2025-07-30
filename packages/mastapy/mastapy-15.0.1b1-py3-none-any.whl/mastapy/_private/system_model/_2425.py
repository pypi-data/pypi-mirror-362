"""MeshStiffnessModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MESH_STIFFNESS_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel", "MeshStiffnessModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeshStiffnessModel")
    CastSelf = TypeVar("CastSelf", bound="MeshStiffnessModel._Cast_MeshStiffnessModel")


__docformat__ = "restructuredtext en"
__all__ = ("MeshStiffnessModel",)


class MeshStiffnessModel(Enum):
    """MeshStiffnessModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MESH_STIFFNESS_MODEL

    CONSTANT_IN_LOA = 0
    ADVANCED_SYSTEM_DEFLECTION = 1
    ISO_SIMPLE_CONTINUOUS_MODEL = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MeshStiffnessModel.__setattr__ = __enum_setattr
MeshStiffnessModel.__delattr__ = __enum_delattr
