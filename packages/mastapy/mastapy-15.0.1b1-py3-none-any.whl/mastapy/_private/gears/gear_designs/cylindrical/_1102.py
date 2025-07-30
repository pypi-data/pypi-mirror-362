"""AddendumModificationDistributionRule"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ADDENDUM_MODIFICATION_DISTRIBUTION_RULE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "AddendumModificationDistributionRule"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AddendumModificationDistributionRule")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AddendumModificationDistributionRule._Cast_AddendumModificationDistributionRule",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AddendumModificationDistributionRule",)


class AddendumModificationDistributionRule(Enum):
    """AddendumModificationDistributionRule

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ADDENDUM_MODIFICATION_DISTRIBUTION_RULE

    USERSPECIFIED = 0
    ZERO_PINION_PROFILE_SHIFT_COEFFICIENT = 1
    GENERAL_APPLICATIONS = 2
    EQUAL_BENDING_STRENGTH = 3
    BALANCE_SLIDE_ROLL_RATIOS = 4
    INCREASING_SPEED = 5
    AVOID_UNDERCUT = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AddendumModificationDistributionRule.__setattr__ = __enum_setattr
AddendumModificationDistributionRule.__delattr__ = __enum_delattr
