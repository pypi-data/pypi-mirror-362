"""GearMeshStiffnessModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_MESH_STIFFNESS_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "GearMeshStiffnessModel"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMeshStiffnessModel")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshStiffnessModel._Cast_GearMeshStiffnessModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshStiffnessModel",)


class GearMeshStiffnessModel(Enum):
    """GearMeshStiffnessModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_MESH_STIFFNESS_MODEL

    LOAD_CASE_SETTING = 0
    SIMPLE_STIFFNESS = 1
    BASIC_LTCA = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearMeshStiffnessModel.__setattr__ = __enum_setattr
GearMeshStiffnessModel.__delattr__ = __enum_delattr
