"""ISO76StaticSafetyFactorLimits"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ISO76_STATIC_SAFETY_FACTOR_LIMITS = python_net_import(
    "SMT.MastaAPI.Materials", "ISO76StaticSafetyFactorLimits"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISO76StaticSafetyFactorLimits")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO76StaticSafetyFactorLimits._Cast_ISO76StaticSafetyFactorLimits",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO76StaticSafetyFactorLimits",)


class ISO76StaticSafetyFactorLimits(Enum):
    """ISO76StaticSafetyFactorLimits

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ISO76_STATIC_SAFETY_FACTOR_LIMITS

    QUIETRUNNING_APPLICATIONS_SMOOTHRUNNING_VIBRATIONFREE_HIGH_ROTATIONAL_ACCURACY = 0
    NORMALRUNNING_APPLICATIONS_SMOOTHRUNNING_VIBRATIONFREE_NORMAL_ROTATIONAL_ACCURACY = 1
    APPLICATIONS_SUBJECTED_TO_SHOCK_LOADS_PRONOUNCED_SHOCK_LOADS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ISO76StaticSafetyFactorLimits.__setattr__ = __enum_setattr
ISO76StaticSafetyFactorLimits.__delattr__ = __enum_delattr
