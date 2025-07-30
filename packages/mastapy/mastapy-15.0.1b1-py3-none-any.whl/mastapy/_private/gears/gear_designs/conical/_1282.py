"""CutterGaugeLengths"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CUTTER_GAUGE_LENGTHS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "CutterGaugeLengths"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CutterGaugeLengths")
    CastSelf = TypeVar("CastSelf", bound="CutterGaugeLengths._Cast_CutterGaugeLengths")


__docformat__ = "restructuredtext en"
__all__ = ("CutterGaugeLengths",)


class CutterGaugeLengths(Enum):
    """CutterGaugeLengths

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CUTTER_GAUGE_LENGTHS

    _1143MM = 0
    _92075MM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CutterGaugeLengths.__setattr__ = __enum_setattr
CutterGaugeLengths.__delattr__ = __enum_delattr
