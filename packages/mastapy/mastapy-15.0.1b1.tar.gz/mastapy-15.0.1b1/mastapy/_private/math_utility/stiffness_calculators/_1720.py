"""IndividualContactPosition"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INDIVIDUAL_CONTACT_POSITION = python_net_import(
    "SMT.MastaAPI.MathUtility.StiffnessCalculators", "IndividualContactPosition"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IndividualContactPosition")
    CastSelf = TypeVar(
        "CastSelf", bound="IndividualContactPosition._Cast_IndividualContactPosition"
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndividualContactPosition",)


class IndividualContactPosition(Enum):
    """IndividualContactPosition

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INDIVIDUAL_CONTACT_POSITION

    LEFT_FLANK = 0
    MAJOR_DIAMETER = 1
    RIGHT_FLANK = 2
    MINOR_DIAMETER = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


IndividualContactPosition.__setattr__ = __enum_setattr
IndividualContactPosition.__delattr__ = __enum_delattr
