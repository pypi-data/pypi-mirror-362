"""MeshingDiameterForGear"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MESHING_DIAMETER_FOR_GEAR = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "MeshingDiameterForGear"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeshingDiameterForGear")
    CastSelf = TypeVar(
        "CastSelf", bound="MeshingDiameterForGear._Cast_MeshingDiameterForGear"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeshingDiameterForGear",)


class MeshingDiameterForGear(Enum):
    """MeshingDiameterForGear

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MESHING_DIAMETER_FOR_GEAR

    ROOT_DIAMETER = 0
    TIP_DIAMETER = 1
    REFERENCE_DIAMETER = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MeshingDiameterForGear.__setattr__ = __enum_setattr
MeshingDiameterForGear.__delattr__ = __enum_delattr
