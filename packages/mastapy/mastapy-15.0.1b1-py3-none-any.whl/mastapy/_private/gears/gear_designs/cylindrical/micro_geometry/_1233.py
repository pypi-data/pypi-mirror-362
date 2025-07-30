"""MeasuredMapDataTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MEASURED_MAP_DATA_TYPES = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry", "MeasuredMapDataTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MeasuredMapDataTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="MeasuredMapDataTypes._Cast_MeasuredMapDataTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MeasuredMapDataTypes",)


class MeasuredMapDataTypes(Enum):
    """MeasuredMapDataTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MEASURED_MAP_DATA_TYPES

    MULTIPLE_PROFILES = 0
    MULTIPLE_PROFILES_ONE_LEAD = 1
    MULTIPLE_LEADS = 2
    MULTIPLE_LEADS_ONE_PROFILE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MeasuredMapDataTypes.__setattr__ = __enum_setattr
MeasuredMapDataTypes.__delattr__ = __enum_delattr
