"""AGMALubricantType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AGMA_LUBRICANT_TYPE = python_net_import("SMT.MastaAPI.Materials", "AGMALubricantType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMALubricantType")
    CastSelf = TypeVar("CastSelf", bound="AGMALubricantType._Cast_AGMALubricantType")


__docformat__ = "restructuredtext en"
__all__ = ("AGMALubricantType",)


class AGMALubricantType(Enum):
    """AGMALubricantType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AGMA_LUBRICANT_TYPE

    MINERAL_OIL = 0
    PAO_BASED_SYNTHETIC_NONVI_IMPROVED_OIL = 1
    PAG_BASED_SYNTHETIC = 2
    MILL7808K_GRADE_3 = 3
    MILL7808K_GRADE_4 = 4
    MILL23699E = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AGMALubricantType.__setattr__ = __enum_setattr
AGMALubricantType.__delattr__ = __enum_delattr
