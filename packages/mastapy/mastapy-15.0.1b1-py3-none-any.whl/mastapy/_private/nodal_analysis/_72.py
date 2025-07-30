"""GearMeshContactStatus"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_MESH_CONTACT_STATUS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "GearMeshContactStatus"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMeshContactStatus")
    CastSelf = TypeVar(
        "CastSelf", bound="GearMeshContactStatus._Cast_GearMeshContactStatus"
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshContactStatus",)


class GearMeshContactStatus(Enum):
    """GearMeshContactStatus

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_MESH_CONTACT_STATUS

    NO_CONTACT = 0
    LEFT_FLANK = 1
    BOTH_FLANKS = 2
    RIGHT_FLANK = -1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearMeshContactStatus.__setattr__ = __enum_setattr
GearMeshContactStatus.__delattr__ = __enum_delattr
