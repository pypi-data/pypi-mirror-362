"""ThreeDViewContourOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_THREE_D_VIEW_CONTOUR_OPTION = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "ThreeDViewContourOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ThreeDViewContourOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ThreeDViewContourOption._Cast_ThreeDViewContourOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ThreeDViewContourOption",)


class ThreeDViewContourOption(Enum):
    """ThreeDViewContourOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _THREE_D_VIEW_CONTOUR_OPTION

    NO_CONTOUR = 0
    STRAIN_ENERGY_PER_COMPONENT = 1
    KINETIC_ENERGY_PER_COMPONENT = 2
    STRAIN_ENERGY_PER_ELEMENT = 3
    KINETIC_ENERGY_PER_ELEMENT = 4
    STRAIN_ENERGY_PER_FE_SECTION = 5
    KINETIC_ENERGY_PER_FE_SECTION = 6
    DISPLACEMENT_ANGULAR_MAGNITUDE = 7
    DISPLACEMENT_RADIAL_TILT_MAGNITUDE = 8
    DISPLACEMENT_TWIST = 9
    DISPLACEMENT_LINEAR_MAGNITUDE = 10
    DISPLACEMENT_RADIAL_MAGNITUDE = 11
    DISPLACEMENT_AXIAL = 12
    DISPLACEMENT_LOCAL_X = 13
    DISPLACEMENT_LOCAL_Y = 14
    DISPLACEMENT_LOCAL_Z = 15
    DISPLACEMENT_GLOBAL_X = 16
    DISPLACEMENT_GLOBAL_Y = 17
    DISPLACEMENT_GLOBAL_Z = 18
    FORCE_ANGULAR_MAGNITUDE = 19
    FORCE_TORQUE = 20
    FORCE_LINEAR_MAGNITUDE = 21
    FORCE_RADIAL_MAGNITUDE = 22
    FORCE_AXIAL = 23
    STRESS_NOMINAL_AXIAL = 24
    STRESS_NOMINAL_BENDING = 25
    STRESS_NOMINAL_TORSIONAL = 26
    STRESS_NOMINAL_VON_MISES_ALTERNATING = 27
    STRESS_NOMINAL_VON_MISES_MAX = 28
    STRESS_NOMINAL_VON_MISES_MEAN = 29
    STRESS_NOMINAL_MAXIMUM_PRINCIPAL = 30
    STRESS_NOMINAL_MINIMUM_PRINCIPAL = 31
    FE_MESH_NORMAL_DISPLACEMENT = 32
    FE_MESH_NORMAL_VELOCITY = 33
    FE_MESH_NORMAL_ACCELERATION = 34
    SOUND_PRESSURE = 35


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ThreeDViewContourOption.__setattr__ = __enum_setattr
ThreeDViewContourOption.__delattr__ = __enum_delattr
