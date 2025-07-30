"""RigidConnectorTiltStiffnessTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RIGID_CONNECTOR_TILT_STIFFNESS_TYPES = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RigidConnectorTiltStiffnessTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RigidConnectorTiltStiffnessTypes")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidConnectorTiltStiffnessTypes._Cast_RigidConnectorTiltStiffnessTypes",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidConnectorTiltStiffnessTypes",)


class RigidConnectorTiltStiffnessTypes(Enum):
    """RigidConnectorTiltStiffnessTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RIGID_CONNECTOR_TILT_STIFFNESS_TYPES

    SINGLE_NODE_WITH_SPECIFIED_STIFFNESS = 0
    DERIVED_FROM_LENGTH_AND_RADIAL_STIFFNESS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RigidConnectorTiltStiffnessTypes.__setattr__ = __enum_setattr
RigidConnectorTiltStiffnessTypes.__delattr__ = __enum_delattr
