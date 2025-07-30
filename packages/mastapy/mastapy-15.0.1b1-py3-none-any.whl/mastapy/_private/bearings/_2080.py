"""BearingModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_MODEL = python_net_import("SMT.MastaAPI.Bearings", "BearingModel")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingModel")
    CastSelf = TypeVar("CastSelf", bound="BearingModel._Cast_BearingModel")


__docformat__ = "restructuredtext en"
__all__ = ("BearingModel",)


class BearingModel(Enum):
    """BearingModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_MODEL

    CONCEPT_BEARING = 0
    AXIAL_CLEARANCE_BEARING = 1
    RADIAL_CLEARANCE_BEARING = 2
    ROLLING_BEARING = 3
    PLAIN_JOURNAL_BEARING = 4
    TILTING_PAD_THRUST_BEARING = 5
    TILTING_PAD_JOURNAL_BEARING = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingModel.__setattr__ = __enum_setattr
BearingModel.__delattr__ = __enum_delattr
