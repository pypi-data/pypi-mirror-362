"""JointGeometries"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_JOINT_GEOMETRIES = python_net_import("SMT.MastaAPI.Bolts", "JointGeometries")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="JointGeometries")
    CastSelf = TypeVar("CastSelf", bound="JointGeometries._Cast_JointGeometries")


__docformat__ = "restructuredtext en"
__all__ = ("JointGeometries",)


class JointGeometries(Enum):
    """JointGeometries

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _JOINT_GEOMETRIES

    PRISMATIC_BODY = 0
    BEAM = 1
    CIRCULAR_PLATE = 2
    FLANGE = 3
    SYMMETRIC_MULTI_BOLTED_JOINT = 4
    ASYMMETRIC_MULTI_BOLTED_JOINT = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


JointGeometries.__setattr__ = __enum_setattr
JointGeometries.__delattr__ = __enum_delattr
