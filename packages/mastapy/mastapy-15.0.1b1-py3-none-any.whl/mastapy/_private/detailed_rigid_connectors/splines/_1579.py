"""DudleyEffectiveLengthApproximationOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DUDLEY_EFFECTIVE_LENGTH_APPROXIMATION_OPTION = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines",
    "DudleyEffectiveLengthApproximationOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DudleyEffectiveLengthApproximationOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DudleyEffectiveLengthApproximationOption._Cast_DudleyEffectiveLengthApproximationOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DudleyEffectiveLengthApproximationOption",)


class DudleyEffectiveLengthApproximationOption(Enum):
    """DudleyEffectiveLengthApproximationOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DUDLEY_EFFECTIVE_LENGTH_APPROXIMATION_OPTION

    FOR_MAXIMUM_MISALIGNMENT = 0
    FOR_MODERATE_MISALIGNMENT = 1
    FOR_FLEXIBLE_SPLINES = 2
    FOR_FIXED_SPLINES_WITH_HELIX_MODIFICATION = 3
    FOR_FIXED_SPLINES_WITHOUT_HELIX_MODIFICATION = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DudleyEffectiveLengthApproximationOption.__setattr__ = __enum_setattr
DudleyEffectiveLengthApproximationOption.__delattr__ = __enum_delattr
