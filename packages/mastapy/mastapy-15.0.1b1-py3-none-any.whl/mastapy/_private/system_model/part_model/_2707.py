"""ShaftDiameterModificationDueToRollingBearingRing"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SHAFT_DIAMETER_MODIFICATION_DUE_TO_ROLLING_BEARING_RING = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel",
    "ShaftDiameterModificationDueToRollingBearingRing",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ShaftDiameterModificationDueToRollingBearingRing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftDiameterModificationDueToRollingBearingRing._Cast_ShaftDiameterModificationDueToRollingBearingRing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDiameterModificationDueToRollingBearingRing",)


class ShaftDiameterModificationDueToRollingBearingRing(Enum):
    """ShaftDiameterModificationDueToRollingBearingRing

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SHAFT_DIAMETER_MODIFICATION_DUE_TO_ROLLING_BEARING_RING

    PRESERVE_RING_MASS = 0
    USE_RACE_DIAMETER = 1
    IGNORE_BEARING_RING = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ShaftDiameterModificationDueToRollingBearingRing.__setattr__ = __enum_setattr
ShaftDiameterModificationDueToRollingBearingRing.__delattr__ = __enum_delattr
