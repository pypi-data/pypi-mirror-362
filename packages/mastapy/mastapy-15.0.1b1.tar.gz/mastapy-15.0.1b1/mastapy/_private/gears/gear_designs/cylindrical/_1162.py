"""HardnessProfileCalculationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HARDNESS_PROFILE_CALCULATION_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "HardnessProfileCalculationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HardnessProfileCalculationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HardnessProfileCalculationMethod._Cast_HardnessProfileCalculationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HardnessProfileCalculationMethod",)


class HardnessProfileCalculationMethod(Enum):
    """HardnessProfileCalculationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HARDNESS_PROFILE_CALCULATION_METHOD

    MACKALDENER = 0
    TOBE = 1
    LANG = 2
    THOMAS = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HardnessProfileCalculationMethod.__setattr__ = __enum_setattr
HardnessProfileCalculationMethod.__delattr__ = __enum_delattr
