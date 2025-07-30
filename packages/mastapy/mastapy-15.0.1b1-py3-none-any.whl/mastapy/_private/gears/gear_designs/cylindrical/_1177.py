"""PlanetGearSetPhaseRequirement"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PLANET_GEAR_SET_PHASE_REQUIREMENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "PlanetGearSetPhaseRequirement"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PlanetGearSetPhaseRequirement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlanetGearSetPhaseRequirement._Cast_PlanetGearSetPhaseRequirement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlanetGearSetPhaseRequirement",)


class PlanetGearSetPhaseRequirement(Enum):
    """PlanetGearSetPhaseRequirement

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PLANET_GEAR_SET_PHASE_REQUIREMENT

    IN_PHASE = 0
    OUT_OF_PHASE = 1
    IGNORE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PlanetGearSetPhaseRequirement.__setattr__ = __enum_setattr
PlanetGearSetPhaseRequirement.__delattr__ = __enum_delattr
