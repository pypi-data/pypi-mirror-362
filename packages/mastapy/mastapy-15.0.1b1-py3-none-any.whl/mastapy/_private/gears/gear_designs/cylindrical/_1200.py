"""TypeOfMechanismHousing"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TYPE_OF_MECHANISM_HOUSING = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "TypeOfMechanismHousing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TypeOfMechanismHousing")
    CastSelf = TypeVar(
        "CastSelf", bound="TypeOfMechanismHousing._Cast_TypeOfMechanismHousing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TypeOfMechanismHousing",)


class TypeOfMechanismHousing(Enum):
    """TypeOfMechanismHousing

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TYPE_OF_MECHANISM_HOUSING

    OPEN_WITH_UNIMPEDED_ENTRY_OF_AIR = 0
    PARTIALLY_OPEN_HOUSING_SPECIFY_A_PERCENTAGE = 1
    CLOSED_HOUSING = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TypeOfMechanismHousing.__setattr__ = __enum_setattr
TypeOfMechanismHousing.__delattr__ = __enum_delattr
