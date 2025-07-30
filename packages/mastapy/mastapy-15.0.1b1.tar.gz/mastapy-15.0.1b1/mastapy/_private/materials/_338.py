"""CylindricalGearRatingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_RATING_METHODS = python_net_import(
    "SMT.MastaAPI.Materials", "CylindricalGearRatingMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearRatingMethods")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearRatingMethods._Cast_CylindricalGearRatingMethods",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearRatingMethods",)


class CylindricalGearRatingMethods(Enum):
    """CylindricalGearRatingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_GEAR_RATING_METHODS

    STANDARD_WITHDRAWN = 0
    AGMA_2101D04 = 1
    ISO_63362019 = 2
    ISO_63362006 = 3
    ISO_63361996 = 4
    DIN_39901987 = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalGearRatingMethods.__setattr__ = __enum_setattr
CylindricalGearRatingMethods.__delattr__ = __enum_delattr
