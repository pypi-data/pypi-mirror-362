"""CoolingDuctShape"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COOLING_DUCT_SHAPE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "CoolingDuctShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CoolingDuctShape")
    CastSelf = TypeVar("CastSelf", bound="CoolingDuctShape._Cast_CoolingDuctShape")


__docformat__ = "restructuredtext en"
__all__ = ("CoolingDuctShape",)


class CoolingDuctShape(Enum):
    """CoolingDuctShape

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COOLING_DUCT_SHAPE

    CIRCULAR = 0
    ELLIPSE = 1
    RECTANGULAR = 2
    TYPE_1 = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CoolingDuctShape.__setattr__ = __enum_setattr
CoolingDuctShape.__delattr__ = __enum_delattr
