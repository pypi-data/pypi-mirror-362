"""RigidCouplingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RIGID_COUPLING_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.DevToolsAnalyses", "RigidCouplingType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RigidCouplingType")
    CastSelf = TypeVar("CastSelf", bound="RigidCouplingType._Cast_RigidCouplingType")


__docformat__ = "restructuredtext en"
__all__ = ("RigidCouplingType",)


class RigidCouplingType(Enum):
    """RigidCouplingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RIGID_COUPLING_TYPE

    KINEMATIC = 0
    DISTRIBUTING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RigidCouplingType.__setattr__ = __enum_setattr
RigidCouplingType.__delattr__ = __enum_delattr
