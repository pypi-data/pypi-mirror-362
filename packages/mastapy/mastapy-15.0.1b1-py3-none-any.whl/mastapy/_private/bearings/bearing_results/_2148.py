"""CylindricalRollerMaxAxialLoadMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_ROLLER_MAX_AXIAL_LOAD_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "CylindricalRollerMaxAxialLoadMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalRollerMaxAxialLoadMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalRollerMaxAxialLoadMethod._Cast_CylindricalRollerMaxAxialLoadMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalRollerMaxAxialLoadMethod",)


class CylindricalRollerMaxAxialLoadMethod(Enum):
    """CylindricalRollerMaxAxialLoadMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_ROLLER_MAX_AXIAL_LOAD_METHOD

    NONE = 0
    SKF = 1
    NACHI = 2
    SCHAEFFLER = 3
    NTN = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalRollerMaxAxialLoadMethod.__setattr__ = __enum_setattr
CylindricalRollerMaxAxialLoadMethod.__delattr__ = __enum_delattr
