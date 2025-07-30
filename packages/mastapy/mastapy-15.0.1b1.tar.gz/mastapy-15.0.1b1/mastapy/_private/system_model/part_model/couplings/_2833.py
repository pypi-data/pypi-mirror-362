"""RigidConnectorStiffnessType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RIGID_CONNECTOR_STIFFNESS_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RigidConnectorStiffnessType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RigidConnectorStiffnessType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidConnectorStiffnessType._Cast_RigidConnectorStiffnessType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidConnectorStiffnessType",)


class RigidConnectorStiffnessType(Enum):
    """RigidConnectorStiffnessType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RIGID_CONNECTOR_STIFFNESS_TYPE

    SIMPLE = 0
    SPECIFY_MATRIX = 1
    NONLINEAR = 2
    INDIVIDUAL_CONTACTS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RigidConnectorStiffnessType.__setattr__ = __enum_setattr
RigidConnectorStiffnessType.__delattr__ = __enum_delattr
