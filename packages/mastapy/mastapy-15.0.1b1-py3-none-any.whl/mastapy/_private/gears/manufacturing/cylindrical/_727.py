"""CylindricalMftRoughingMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_MFT_ROUGHING_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "CylindricalMftRoughingMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalMftRoughingMethods")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMftRoughingMethods._Cast_CylindricalMftRoughingMethods",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMftRoughingMethods",)


class CylindricalMftRoughingMethods(Enum):
    """CylindricalMftRoughingMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_MFT_ROUGHING_METHODS

    HOBBING = 0
    SHAPING = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalMftRoughingMethods.__setattr__ = __enum_setattr
CylindricalMftRoughingMethods.__delattr__ = __enum_delattr
