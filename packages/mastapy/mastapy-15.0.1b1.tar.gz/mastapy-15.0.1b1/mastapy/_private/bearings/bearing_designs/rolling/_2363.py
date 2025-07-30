"""FourPointContactAngleDefinition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FOUR_POINT_CONTACT_ANGLE_DEFINITION = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "FourPointContactAngleDefinition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FourPointContactAngleDefinition")
    CastSelf = TypeVar(
        "CastSelf",
        bound="FourPointContactAngleDefinition._Cast_FourPointContactAngleDefinition",
    )


__docformat__ = "restructuredtext en"
__all__ = ("FourPointContactAngleDefinition",)


class FourPointContactAngleDefinition(Enum):
    """FourPointContactAngleDefinition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FOUR_POINT_CONTACT_ANGLE_DEFINITION

    AXIAL = 0
    RADIAL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FourPointContactAngleDefinition.__setattr__ = __enum_setattr
FourPointContactAngleDefinition.__delattr__ = __enum_delattr
