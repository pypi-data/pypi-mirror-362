"""HarmonicExcitationType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HARMONIC_EXCITATION_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads", "HarmonicExcitationType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicExcitationType")
    CastSelf = TypeVar(
        "CastSelf", bound="HarmonicExcitationType._Cast_HarmonicExcitationType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicExcitationType",)


class HarmonicExcitationType(Enum):
    """HarmonicExcitationType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HARMONIC_EXCITATION_TYPE

    NONE = 0
    BASIC_LTCA = 1
    ADVANCED_LTCA = 2
    TCA = 3
    ADVANCED_SYSTEM_DEFLECTION_CURRENT_LOAD_CASE_SET_UP = 4
    ADVANCED_SYSTEM_DEFLECTION_SINGLE_TOOTH_PASS_USING_BASIC_LTCA = 5
    ADVANCED_SYSTEM_DEFLECTION_SINGLE_TOOTH_PASS_USING_ADVANCED_LTCA = 6
    UNIT_FIRST_HARMONIC_TE = 7
    USERSPECIFIED = 8
    LOAD_CASE_TIME_VARYING_LOAD = 9
    LOAD_CASE_ANGLE_VARYING_LOAD = 10
    GLEASON_CAGE_TCA = 11
    GLEASON_CAGE_LTCA = 12
    CALCULATED = 13
    UNIT_HARMONIC_FORCE_FRF = 14
    UNIT_HARMONIC_MOMENT_FRF = 15
    ELECTRIC_MACHINE_SPEED_DEPENDENT_ROTOR_AND_STATOR_LOADS = 16
    KIMOS_XML = 17
    GLEASON_GEMS_XML = 18


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HarmonicExcitationType.__setattr__ = __enum_setattr
HarmonicExcitationType.__delattr__ = __enum_delattr
