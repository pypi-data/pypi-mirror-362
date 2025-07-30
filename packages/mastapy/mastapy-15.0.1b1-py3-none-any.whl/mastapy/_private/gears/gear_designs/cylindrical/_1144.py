"""CylindricalGearTableMGItemDetail"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_TABLE_MG_ITEM_DETAIL = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearTableMGItemDetail"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalGearTableMGItemDetail")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearTableMGItemDetail._Cast_CylindricalGearTableMGItemDetail",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearTableMGItemDetail",)


class CylindricalGearTableMGItemDetail(Enum):
    """CylindricalGearTableMGItemDetail

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_GEAR_TABLE_MG_ITEM_DETAIL

    CHART = 0
    REPORT = 1
    REPORT_AND_CHART = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalGearTableMGItemDetail.__setattr__ = __enum_setattr
CylindricalGearTableMGItemDetail.__delattr__ = __enum_delattr
