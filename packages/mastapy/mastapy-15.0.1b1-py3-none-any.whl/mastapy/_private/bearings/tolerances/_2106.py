"""BearingToleranceClass"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_TOLERANCE_CLASS = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "BearingToleranceClass"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingToleranceClass")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingToleranceClass._Cast_BearingToleranceClass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingToleranceClass",)


class BearingToleranceClass(Enum):
    """BearingToleranceClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_TOLERANCE_CLASS

    CLASS_0_RADIAL_METRIC = 0
    CLASS_6_RADIAL_METRIC = 1
    CLASS_5_RADIAL_METRIC = 2
    CLASS_4_RADIAL_METRIC = 3
    CLASS_2_RADIAL_METRIC = 4
    CLASS_0_6X_RADIAL_METRIC_TAPER = 5
    CLASS_5_RADIAL_METRIC_TAPER = 6
    CLASS_4_RADIAL_METRIC_TAPER = 7
    CLASS_2_RADIAL_METRIC_TAPER = 8
    CLASS_K_RADIAL_METRIC_TIMKEN = 9
    CLASS_N_RADIAL_METRIC_TIMKEN = 10
    CLASS_C_RADIAL_METRIC_TIMKEN = 11
    CLASS_B_RADIAL_METRIC_TIMKEN = 12
    CLASS_A_RADIAL_METRIC_TIMKEN = 13
    CLASS_4_RADIAL_INCH_TAPER = 14
    CLASS_2_RADIAL_INCH_TAPER = 15
    CLASS_3_RADIAL_INCH_TAPER = 16
    CLASS_0_RADIAL_INCH_TAPER = 17
    CLASS_00_RADIAL_INCH_TAPER = 18
    CLASS_0_THRUST_METRIC = 19
    CLASS_6_THRUST_METRIC = 20
    CLASS_5_THRUST_METRIC = 21
    CLASS_4_THRUST_METRIC = 22


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingToleranceClass.__setattr__ = __enum_setattr
BearingToleranceClass.__delattr__ = __enum_delattr
