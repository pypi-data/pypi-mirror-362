"""GearMeshEfficiencyRatingMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_GEAR_MESH_EFFICIENCY_RATING_METHOD = python_net_import(
    "SMT.MastaAPI.Gears.Rating", "GearMeshEfficiencyRatingMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="GearMeshEfficiencyRatingMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshEfficiencyRatingMethod._Cast_GearMeshEfficiencyRatingMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshEfficiencyRatingMethod",)


class GearMeshEfficiencyRatingMethod(Enum):
    """GearMeshEfficiencyRatingMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _GEAR_MESH_EFFICIENCY_RATING_METHOD

    ISOTR_1417912001 = 0
    ISOTR_1417922001 = 1
    USERSPECIFIED_TOOTH_LOSS_FACTOR = 2
    VELEX_AND_VILLE = 3
    HENRIOT = 4
    BUCKINGHAM = 5
    LTCA_MEAN_SLIDING_POWER_LOSS = 6
    SCRIPT = 7


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


GearMeshEfficiencyRatingMethod.__setattr__ = __enum_setattr
GearMeshEfficiencyRatingMethod.__delattr__ = __enum_delattr
