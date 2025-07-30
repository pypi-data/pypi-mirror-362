"""BacklashDistributionRule"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BACKLASH_DISTRIBUTION_RULE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Conical", "BacklashDistributionRule"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BacklashDistributionRule")
    CastSelf = TypeVar(
        "CastSelf", bound="BacklashDistributionRule._Cast_BacklashDistributionRule"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BacklashDistributionRule",)


class BacklashDistributionRule(Enum):
    """BacklashDistributionRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BACKLASH_DISTRIBUTION_RULE

    AUTO = 0
    ALL_ON_PINION = 1
    ALL_ON_WHEEL = 2
    DISTRIBUTED_EQUALLY = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BacklashDistributionRule.__setattr__ = __enum_setattr
BacklashDistributionRule.__delattr__ = __enum_delattr
