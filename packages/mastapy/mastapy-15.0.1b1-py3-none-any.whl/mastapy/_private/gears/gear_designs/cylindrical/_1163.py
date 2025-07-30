"""HeatTreatmentType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HEAT_TREATMENT_TYPE = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "HeatTreatmentType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HeatTreatmentType")
    CastSelf = TypeVar("CastSelf", bound="HeatTreatmentType._Cast_HeatTreatmentType")


__docformat__ = "restructuredtext en"
__all__ = ("HeatTreatmentType",)


class HeatTreatmentType(Enum):
    """HeatTreatmentType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HEAT_TREATMENT_TYPE

    CARBURIZING = 0
    NITRIDING = 1
    INDUCTION_OR_FLAME = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HeatTreatmentType.__setattr__ = __enum_setattr
HeatTreatmentType.__delattr__ = __enum_delattr
