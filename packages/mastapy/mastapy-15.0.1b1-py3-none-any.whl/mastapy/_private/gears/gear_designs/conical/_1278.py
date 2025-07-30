"""ConicalManufactureMethods"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONICAL_MANUFACTURE_METHODS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "ConicalManufactureMethods"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ConicalManufactureMethods")
    CastSelf = TypeVar(
        "CastSelf", bound="ConicalManufactureMethods._Cast_ConicalManufactureMethods"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ConicalManufactureMethods",)


class ConicalManufactureMethods(Enum):
    """ConicalManufactureMethods

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONICAL_MANUFACTURE_METHODS

    FORMATE_TILT = 0
    FORMATE_MODIFIED_ROLL = 1
    GENERATING_TILT = 2
    GENERATING_TILT_WITH_OFFSET = 3
    GENERATING_MODIFIED_ROLL = 4
    HELIXFORM = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ConicalManufactureMethods.__setattr__ = __enum_setattr
ConicalManufactureMethods.__delattr__ = __enum_delattr
