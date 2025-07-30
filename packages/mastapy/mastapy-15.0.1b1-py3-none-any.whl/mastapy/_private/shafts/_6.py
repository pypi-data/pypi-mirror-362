"""AGMAHardeningType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_AGMA_HARDENING_TYPE = python_net_import("SMT.MastaAPI.Shafts", "AGMAHardeningType")

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AGMAHardeningType")
    CastSelf = TypeVar("CastSelf", bound="AGMAHardeningType._Cast_AGMAHardeningType")


__docformat__ = "restructuredtext en"
__all__ = ("AGMAHardeningType",)


class AGMAHardeningType(Enum):
    """AGMAHardeningType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _AGMA_HARDENING_TYPE

    DUCTILE_THROUGH_HARDENED_STEEL = 0
    SURFACE_HARDENED_STEEL = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AGMAHardeningType.__setattr__ = __enum_setattr
AGMAHardeningType.__delattr__ = __enum_delattr
