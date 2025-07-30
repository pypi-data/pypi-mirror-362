"""MaterialStandards"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MATERIAL_STANDARDS = python_net_import("SMT.MastaAPI.Materials", "MaterialStandards")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaterialStandards")
    CastSelf = TypeVar("CastSelf", bound="MaterialStandards._Cast_MaterialStandards")


__docformat__ = "restructuredtext en"
__all__ = ("MaterialStandards",)


class MaterialStandards(Enum):
    """MaterialStandards

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MATERIAL_STANDARDS

    CUSTOM = 0
    EN_10083 = 1
    ASTM_A48 = 2
    ASTM_A536 = 3
    GBT_3077 = 4
    EN_10084 = 5
    GBT_1348 = 6
    JIS_G_4051 = 7
    JIS_G_4052 = 8
    JIS_G_4104 = 9
    JIS_G_4105 = 10
    VDI_2736_PART_1 = 11


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MaterialStandards.__setattr__ = __enum_setattr
MaterialStandards.__delattr__ = __enum_delattr
