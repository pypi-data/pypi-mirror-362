"""LubricantViscosityClassSAE"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LUBRICANT_VISCOSITY_CLASS_SAE = python_net_import(
    "SMT.MastaAPI.Materials", "LubricantViscosityClassSAE"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LubricantViscosityClassSAE")
    CastSelf = TypeVar(
        "CastSelf", bound="LubricantViscosityClassSAE._Cast_LubricantViscosityClassSAE"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LubricantViscosityClassSAE",)


class LubricantViscosityClassSAE(Enum):
    """LubricantViscosityClassSAE

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LUBRICANT_VISCOSITY_CLASS_SAE

    _0W5W = 0
    _10W = 1
    _15W = 2
    _20 = 3
    _20W = 4
    _25W = 5
    _30 = 6
    _40 = 7
    _50 = 8
    _60 = 9
    _70W = 10
    _75W = 11
    _80 = 12
    _80W = 13
    _85 = 14
    _85W = 15
    _90 = 16
    _110 = 17
    _140 = 18
    _190 = 19
    _250 = 20


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LubricantViscosityClassSAE.__setattr__ = __enum_setattr
LubricantViscosityClassSAE.__delattr__ = __enum_delattr
