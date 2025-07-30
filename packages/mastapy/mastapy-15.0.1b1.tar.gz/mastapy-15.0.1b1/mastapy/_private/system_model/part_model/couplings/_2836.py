"""RigidConnectorToothSpacingType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RIGID_CONNECTOR_TOOTH_SPACING_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "RigidConnectorToothSpacingType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RigidConnectorToothSpacingType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RigidConnectorToothSpacingType._Cast_RigidConnectorToothSpacingType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RigidConnectorToothSpacingType",)


class RigidConnectorToothSpacingType(Enum):
    """RigidConnectorToothSpacingType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RIGID_CONNECTOR_TOOTH_SPACING_TYPE

    EQUALLYSPACED_TEETH = 0
    CUSTOM_SPACING_OF_TEETH = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RigidConnectorToothSpacingType.__setattr__ = __enum_setattr
RigidConnectorToothSpacingType.__delattr__ = __enum_delattr
