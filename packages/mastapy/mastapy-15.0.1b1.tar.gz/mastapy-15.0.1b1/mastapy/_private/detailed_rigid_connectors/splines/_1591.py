"""SAEFatigueLifeFactorTypes"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SAE_FATIGUE_LIFE_FACTOR_TYPES = python_net_import(
    "SMT.MastaAPI.DetailedRigidConnectors.Splines", "SAEFatigueLifeFactorTypes"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SAEFatigueLifeFactorTypes")
    CastSelf = TypeVar(
        "CastSelf", bound="SAEFatigueLifeFactorTypes._Cast_SAEFatigueLifeFactorTypes"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SAEFatigueLifeFactorTypes",)


class SAEFatigueLifeFactorTypes(Enum):
    """SAEFatigueLifeFactorTypes

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SAE_FATIGUE_LIFE_FACTOR_TYPES

    UNIDIRECTIONAL = 0
    FULLY_REVERSED = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SAEFatigueLifeFactorTypes.__setattr__ = __enum_setattr
SAEFatigueLifeFactorTypes.__delattr__ = __enum_delattr
