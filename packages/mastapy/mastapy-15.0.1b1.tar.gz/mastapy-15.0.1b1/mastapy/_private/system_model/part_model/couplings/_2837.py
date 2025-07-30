"""RigidConnectorTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RIGID_CONNECTOR_TYPES = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RigidConnectorTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RigidConnectorTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="RigidConnectorTypes._Cast_RigidConnectorTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidConnectorTypes",)


class RigidConnectorTypes(Enum):
    """RigidConnectorTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RIGID_CONNECTOR_TYPES

    CONCEPT_SPLINE = 0
    DETAILED_SPLINE = 1
    RIGID_BOND = 2
    DETAILED_INTERFERENCE_FIT = 3
    DETAILED_KEYED_JOINT = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RigidConnectorTypes.__setattr__ = __enum_setattr
RigidConnectorTypes.__delattr__ = __enum_delattr
