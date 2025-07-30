"""AcousticRadiationEfficiencyInputType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACOUSTIC_RADIATION_EFFICIENCY_INPUT_TYPE = python_net_import(
    "SMT.MastaAPI.Materials", "AcousticRadiationEfficiencyInputType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticRadiationEfficiencyInputType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="AcousticRadiationEfficiencyInputType._Cast_AcousticRadiationEfficiencyInputType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticRadiationEfficiencyInputType",)


class AcousticRadiationEfficiencyInputType(Enum):
    """AcousticRadiationEfficiencyInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACOUSTIC_RADIATION_EFFICIENCY_INPUT_TYPE

    SPECIFY_VALUES = 0
    SIMPLE_PARAMETRISED = 1
    UNITY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AcousticRadiationEfficiencyInputType.__setattr__ = __enum_setattr
AcousticRadiationEfficiencyInputType.__delattr__ = __enum_delattr
