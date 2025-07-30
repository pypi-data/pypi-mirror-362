"""HeatTreatmentTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEAT_TREATMENT_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "HeatTreatmentTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeatTreatmentTypes")
    CastSelf = TypeVar("CastSelf", bound="HeatTreatmentTypes._Cast_HeatTreatmentTypes")


__docformat__ = "restructuredtext en"
__all__ = ("HeatTreatmentTypes",)


class HeatTreatmentTypes(Enum):
    """HeatTreatmentTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEAT_TREATMENT_TYPES

    NO_HEAT_TREATMENT = 0
    QUENCHED_TEMPERED = 1
    SURFACE_HARDENED = 2
    NITRIDED = 3
    CARBURIZED = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeatTreatmentTypes.__setattr__ = __enum_setattr
HeatTreatmentTypes.__delattr__ = __enum_delattr
