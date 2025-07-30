"""ISOLubricantType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ISO_LUBRICANT_TYPE = python_net_import("SMT.MastaAPI.Materials", "ISOLubricantType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISOLubricantType")
    CastSelf = TypeVar("CastSelf", bound="ISOLubricantType._Cast_ISOLubricantType")


__docformat__ = "restructuredtext en"
__all__ = ("ISOLubricantType",)


class ISOLubricantType(Enum):
    """ISOLubricantType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ISO_LUBRICANT_TYPE

    MINERAL_OIL = 0
    WATER_SOLUBLE_POLYGLYCOL = 1
    NON_WATER_SOLUBLE_POLYGLYCOL = 2
    POLYALPHAOLEFIN = 3
    PHOSPHATE_ESTER = 4
    TRACTION_FLUID = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ISOLubricantType.__setattr__ = __enum_setattr
ISOLubricantType.__delattr__ = __enum_delattr
