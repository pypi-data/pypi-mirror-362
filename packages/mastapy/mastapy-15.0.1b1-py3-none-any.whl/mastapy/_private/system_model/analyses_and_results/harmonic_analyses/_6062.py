"""HarmonicAnalysisTorqueInputType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_HARMONIC_ANALYSIS_TORQUE_INPUT_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses",
    "HarmonicAnalysisTorqueInputType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="HarmonicAnalysisTorqueInputType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="HarmonicAnalysisTorqueInputType._Cast_HarmonicAnalysisTorqueInputType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("HarmonicAnalysisTorqueInputType",)


class HarmonicAnalysisTorqueInputType(Enum):
    """HarmonicAnalysisTorqueInputType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _HARMONIC_ANALYSIS_TORQUE_INPUT_TYPE

    LOAD_CASE = 0
    SPECIFIED_TORQUE_SPEED_CURVE = 1
    TORQUE_SPEED_CURVE_FROM_ELECTRIC_MACHINE_HARMONIC_LOAD_DATA = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


HarmonicAnalysisTorqueInputType.__setattr__ = __enum_setattr
HarmonicAnalysisTorqueInputType.__delattr__ = __enum_delattr
