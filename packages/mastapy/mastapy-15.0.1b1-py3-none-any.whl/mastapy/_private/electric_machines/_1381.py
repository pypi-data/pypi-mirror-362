"""CoreLossBuildFactorSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CORE_LOSS_BUILD_FACTOR_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CoreLossBuildFactorSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoreLossBuildFactorSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CoreLossBuildFactorSpecificationMethod._Cast_CoreLossBuildFactorSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CoreLossBuildFactorSpecificationMethod",)


class CoreLossBuildFactorSpecificationMethod(Enum):
    """CoreLossBuildFactorSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CORE_LOSS_BUILD_FACTOR_SPECIFICATION_METHOD

    STATOR_AND_ROTOR = 0
    HYSTERESIS_EDDY_CURRENT_AND_EXCESS = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoreLossBuildFactorSpecificationMethod.__setattr__ = __enum_setattr
CoreLossBuildFactorSpecificationMethod.__delattr__ = __enum_delattr
