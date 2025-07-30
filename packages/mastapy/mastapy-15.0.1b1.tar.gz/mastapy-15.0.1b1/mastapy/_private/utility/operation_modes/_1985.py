"""OperationMode"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OPERATION_MODE = python_net_import(
    "SMT.MastaAPI.Utility.OperationModes", "OperationMode"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OperationMode")
    CastSelf = TypeVar("CastSelf", bound="OperationMode._Cast_OperationMode")


__docformat__ = "restructuredtext en"
__all__ = ("OperationMode",)


class OperationMode(Enum):
    """OperationMode

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OPERATION_MODE

    UNKNOWN = 0
    DESIGN = 1
    LOAD_CASES_AND_DUTY_CYCLES = 2
    PRODUCT_DATABASE = 3
    FE_PARTS = 4
    ACOUSTIC_ANALYSIS_SETUP = 5
    POWER_FLOW = 6
    SYSTEM_DEFLECTION = 7
    ADVANCED_SYSTEM_DEFLECTION = 8
    HARMONIC_RESPONSE = 9
    NVH_ADVANCED_TIME_STEPPING_ANALYSIS_FOR_MODULATION = 10
    ROTOR_DYNAMICS = 11
    PARAMETRIC_STUDY_TOOL = 12
    SYSTEM_OPTIMISER = 13
    GEAR_MACRO_GEOMETRY = 14
    GEAR_MICRO_GEOMETRY = 15
    CYLINDRICAL_GEAR_MANUFACTURING = 16
    BEVEL_GEAR_MANUFACTURING = 17
    CYCLOIDAL_DESIGN = 18
    DRIVA_LOAD_CASE_SETUP = 19
    DRIVA = 20
    ELECTRIC_MACHINE_DESIGN_ANALYSIS = 21
    THERMAL_ANALYSIS = 22
    BENCHMARKING = 23
    SYNCHRONISER_SHIFT_ANALYSIS = 24
    FLEXIBLE_PIN_ANALYSIS = 25
    MES = 26


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OperationMode.__setattr__ = __enum_setattr
OperationMode.__delattr__ = __enum_delattr
